package com.example

import akka.actor.typed.{ActorRef, ActorSystem}
import akka.actor.typed.scaladsl.AskPattern._
import akka.http.scaladsl.model.StatusCodes
import akka.http.scaladsl.server.Directives._
import akka.http.scaladsl.server.Route
import akka.util.Timeout
import com.example.UserRegistry._

import scala.concurrent.Future

class UserRoutes(userRegistry: ActorRef[UserRegistry.Command])(implicit val system: ActorSystem[_]) {

  import JsonFormats._
  import akka.http.scaladsl.marshallers.sprayjson.SprayJsonSupport._

  // If ask takes more time than this to complete the request is failed
  private implicit val timeout: Timeout = Timeout.create(system.settings.config.getDuration("my-app.routes.ask-timeout"))

  private def getStore(): Future[Store] =
    userRegistry.ask(GetStore.apply)
  private def getPair(key: Int): Future[GetUserResponse] =
    userRegistry.ask(GetPair(key, _))
  private def createPair(key:Int, pair: Pair): Future[ActionPerformed] =
    userRegistry.ask(CreatePair(key, pair, _))
  private def invokeConsensus(txn: Txn): Future[GetConsensusResponse] =
    userRegistry.ask(InvokeConsensus(txn, _))

  val userRoutes: Route =
    pathPrefix("store") {
      concat(
        pathEnd {
          concat(
            get {
              complete(getStore())
            },
            path(Segment) { key =>
              post {
                entity(as[Pair]) { pair =>
                  onSuccess(createPair(key.toInt, pair)) { performed =>
                    complete((StatusCodes.Created, performed))
                  }
                }
              }
            }
          )
        },
        path("get" / IntNumber)  { key =>
            get {
              rejectEmptyResponse {
                onSuccess(getPair(key)) { response =>
                  complete(response.maybePair)
                }
              }
            }
        },
        path("consensus"){
            get {
              entity(as[Txn]) { txn =>
                onSuccess(invokeConsensus(txn)) { response =>
                  complete(response)
                }
              }
            }
        }
      )
    }
}
