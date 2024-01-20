package com.example

import akka.actor.typed.{ActorRef, ActorSystem}
import akka.actor.typed.scaladsl.AskPattern._
import akka.http.scaladsl.model.StatusCodes
import akka.http.scaladsl.server.Directives._
import akka.http.scaladsl.server.Route
import akka.util.Timeout
import com.example.UserRegistry._

import scala.concurrent.Future
import scala.util.{Failure, Success}


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
  private def invokeInconsistenCommit(txn: Txn): Future[Unit] =
    userRegistry.ask(InvokeInconsistenCommit(txn, _))
  private def invokeInconsistenAbort(txn: Txn): Future[Unit] =
    userRegistry.ask(InvokeInconsistenAbort(txn, _))

  val userRoutes: Route =
    pathPrefix("store") {
      concat(
        path("get" / IntNumber)  { key =>
            get {
                onComplete(getPair(key)) {
                  case Success(res) => complete(res.maybePair)
                  case Failure(ex)  => complete(StatusCodes.InternalServerError)
                }
            }
        },
        path("consensus"){
            post {
              entity(as[Txn]) { txn =>
                onComplete(invokeConsensus(txn)){
                  case Success(res) => complete(res)
                  case Failure(ex)  => complete(StatusCodes.InternalServerError)
                }
              }
            }
        }
//        path("inconsistent/commit"){
//          post {
//            entity(as[Txn]) { txn =>
//              onComplete(invokeInconsistenCommit(txn)){
//                case Success(res) => complete(res)
//                case Failure(ex)  => complete(StatusCodes.InternalServerError)
//              }
//            }
//          }
//        },
//        path("inconsistent/abort"){
//          post {
//            entity(as[Txn]) { txn =>
//              onComplete(invokeInconsistenAbort(txn)){
//                case Success(res) => complete(res)
//                case Failure(ex)  => complete(StatusCodes.InternalServerError)
//              }
//            }
//          }
//        }
      )
    }
}
