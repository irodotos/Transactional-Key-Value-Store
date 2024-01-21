package com.example

import akka.actor.typed.ActorRef
import akka.actor.typed.Behavior
import akka.actor.typed.scaladsl.Behaviors

import scala.collection.{immutable, mutable}
import scala.{+:, :+, None}
import spray.json._

import scala.collection.mutable.ArrayBuffer

final case class Pair(key: Int, value: Int, lock: Boolean)
final case class Store(pairs: immutable.Seq[Pair])
final case class KeyValue(method: String, key: Int, value: Int)
final case class Txn(txn: List[KeyValue])

object UserRegistry {
  private val MAP_SIZE = 256

  sealed trait Command
  final case class GetStore(replyTo: ActorRef[Store]) extends Command
  final case class CreatePair(key: Int, pair: Pair, replyTo: ActorRef[ActionPerformed]) extends Command
  final case class GetPair(key: Int, replyTo: ActorRef[GetUserResponse]) extends Command
  final case class InvokeConsensus(txn: Txn, replyTo: ActorRef[GetConsensusResponse]) extends Command
  final case class InvokeInconsistenCommit(txn: Txn, replyTo: ActorRef[String]) extends Command
  final case class InvokeInconsistenAbort(txn: Txn, replyTo: ActorRef[String]) extends Command
  final case class GetUserResponse(maybePair: Option[Pair])
  final case class ActionPerformed(description: String)
  final case class GetConsensusResponse(response: Boolean)

  def apply(): Behavior[Command] = {
    val myMap: Map[Int, Pair] = (0 until MAP_SIZE).map { i =>
      i -> Pair(i, i * 10, false)
    }.toMap
    registry(myMap)
  }

  private def registry(store: Map[Int, Pair]): Behavior[Command] =
    Behaviors.receiveMessage {
      case GetStore(replyTo) =>
        replyTo ! Store(store.values.toSeq)
        Behaviors.same
      case CreatePair(key, pair, replyTo) =>
        replyTo ! ActionPerformed(s"Pair ${pair.key} with value=${pair.value} created.")
        registry(store.updated(key%MAP_SIZE, pair))
      case GetPair(key, replyTo) =>
        replyTo ! GetUserResponse(store.get(key%MAP_SIZE))
        Behaviors.same
      case InvokeConsensus(txn, replyTo) => {
        val getLocks: ArrayBuffer[Boolean] = ArrayBuffer.empty
        txn.txn.map(element => {
          println("element key", element.key%MAP_SIZE)
          val value = store.get(element.key%MAP_SIZE) match {
            case Some(Pair(key, value, lock)) => {
              if(lock == false) {
//                registry(store.updated(key%MAP_SIZE, Pair(key, value, true)))
                store.updated(key%MAP_SIZE, Pair(key, value, true))
                true
              }else{
                false
              }
            }
            case _ => {
              println("WHY AM I HERE???? MAP IS NOT EMPTY")
              false
            }
          }
          getLocks += value
        })
        if(getLocks.contains(false)) replyTo ! GetConsensusResponse(false)
        replyTo ! GetConsensusResponse(true)
        Behaviors.same
      }
      case InvokeInconsistenCommit(txn, replyTo) => {
          txn.txn.map(element => {
            if(element.method == "post") {
              if(store.get(element.key%MAP_SIZE).get.lock == false) println("WHY AM I HERE??? LOCK NEEDS TO BE TRUE COMMIT post")
              store.updated(element.key%256, Pair(element.key, element.value, false))
            }
            else{
              if(store.get(element.key%MAP_SIZE).get.lock == false) println("WHY AM I HERE??? LOCK NEEDS TO BE TRUE COMMIT get")
//              println(store.values.toSeq)
              store.updated(element.key%MAP_SIZE, Pair(element.key%MAP_SIZE, element.value, false))
            }
          })
        replyTo ! "commit completed"
        Behaviors.same
      }
      case InvokeInconsistenAbort(txn, replyTo) => {
        txn.txn.map(element => {
          if(store.get(element.key%MAP_SIZE).get.lock == false) println("WHY AM I HERE??? LOCK NEEDS TO BE TRUE ABORT")
          store.updated(element.key%MAP_SIZE, Pair(element.key, element.value, false))
        })
        replyTo ! "abort completed"
        Behaviors.same
      }
    }
}
