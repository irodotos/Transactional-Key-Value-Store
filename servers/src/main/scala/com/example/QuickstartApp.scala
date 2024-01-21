package com.example

import akka.actor.typed.{ActorSystem, DispatcherSelector}
import akka.actor.typed.scaladsl.Behaviors
import akka.http.scaladsl.Http
import akka.http.scaladsl.server.Route

import scala.util.Failure
import scala.util.Success


object QuickstartApp {

  private def startHttpServer(routes: Route, port: Int)(implicit system: ActorSystem[_]): Unit = {

    import system.executionContext

    val futureBinding = Http().newServerAt("localhost", port).bind(routes)
    futureBinding.onComplete {
      case Success(binding) =>
        val address = binding.localAddress
        system.log.info("Server online at http://{}:{}/", address.getHostString, address.getPort)
      case Failure(ex) =>
        system.log.error("Failed to bind HTTP endpoint, terminating system", ex)
        system.terminate()
    }
  }

  def main(args: Array[String]): Unit = {
    val rootBehavior = Behaviors.setup[Nothing] { context =>
      // spawn the first replica waiting for message in localhost port 8080
      val replica1 = context.spawn(UserRegistry(), "replica1", DispatcherSelector.fromConfig("your-dispatcher"))
      context.watch(replica1)

      val routes1 = new UserRoutes(replica1)(context.system)
      startHttpServer(routes1.userRoutes, 8080)(context.system)

      // spawn the second replica waiting for message in localhost port 8081
      val replica2 = context.spawn(UserRegistry(), "replica2", DispatcherSelector.fromConfig("your-dispatcher"))
      context.watch(replica2)

      val routes2 = new UserRoutes(replica2)(context.system)
      startHttpServer(routes2.userRoutes, 8081)(context.system)

      // spawn the third replica waiting for message in localhost port 8082
      val replica3 = context.spawn(UserRegistry(), "replica3", DispatcherSelector.fromConfig("your-dispatcher"))
      context.watch(replica3)

      val routes3 = new UserRoutes(replica3)(context.system)
      startHttpServer(routes3.userRoutes, 8082)(context.system)

      Behaviors.empty
    }
    val system = ActorSystem[Nothing](rootBehavior, "HelloAkkaHttpServer")
  }
}
