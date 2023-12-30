package com.example

import akka.http.scaladsl.server.Directives._
import akka.http.scaladsl.model.StatusCodes
import akka.http.scaladsl.server.Route

import scala.concurrent.Future
import com.example.UserRegistry._
import akka.actor.typed.ActorRef
import akka.actor.typed.ActorSystem
import akka.actor.typed.scaladsl.AskPattern._
import akka.util.Timeout

class UserRoutes(userRegistry: ActorRef[UserRegistry.Command])(implicit val system: ActorSystem[_]) {

  import akka.http.scaladsl.marshallers.sprayjson.SprayJsonSupport._
  import JsonFormats._

  // If ask takes more time than this to complete the request is failed
  private implicit val timeout: Timeout = Timeout.create(system.settings.config.getDuration("my-app.routes.ask-timeout"))

  def getStore(): Future[Store] =
    userRegistry.ask(GetStore.apply)
  def getPair(key: String): Future[GetUserResponse] =
    userRegistry.ask(GetPair(key, _))
  def createPair(pair: Pair): Future[ActionPerformed] =
    userRegistry.ask(CreatePair(pair, _))
//  def deleteUser(name: String): Future[ActionPerformed] =
//    userRegistry.ask(DeleteUser(name, _))

  val userRoutes: Route =
    pathPrefix("store") {
      concat(
        pathEnd {
          concat(
            get {
              complete(getStore())
            },
            post {
              entity(as[Pair]) { pair =>
                onSuccess(createPair(pair)) { performed =>
                  complete((StatusCodes.Created, performed))
                }
              }
            }
          )
        },
        path(Segment) { key =>
          concat(
            get {
              rejectEmptyResponse {
                onSuccess(getPair(key)) { response =>
                  complete(response.maybePair)
                }
              }
            }
//            delete {
//              //#users-delete-logic
//              onSuccess(deleteUser(name)) { performed =>
//                complete((StatusCodes.OK, performed))
//              }
//            }
          )
        })
    }
}
