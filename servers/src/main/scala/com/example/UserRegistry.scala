package com.example

import akka.actor.typed.ActorRef
import akka.actor.typed.Behavior
import akka.actor.typed.scaladsl.Behaviors

import scala.collection.immutable
import java.util.concurrent.locks.Lock
import scala.{+:, :+, None}
import spray.json._

import scala.collection.mutable.ArrayBuffer

final case class Pair(key: Int, value: Int, lock: Lock)
final case class Store(pairs: immutable.Seq[Pair])
final case class KeyValue(key: Int, value: Int)
final case class Txn(txn: List[KeyValue])

object UserRegistry {
  sealed trait Command
  final case class GetStore(replyTo: ActorRef[Store]) extends Command
  final case class CreatePair(key: Int, pair: Pair, replyTo: ActorRef[ActionPerformed]) extends Command
  final case class GetPair(key: Int, replyTo: ActorRef[GetUserResponse]) extends Command
  final case class InvokeConsensus(txn: Txn, replyTo: ActorRef[GetConsensusResponse]) extends Command
//  final case class DeleteUser(name: String, replyTo: ActorRef[ActionPerformed]) extends Command

  final case class GetUserResponse(maybePair: Option[Pair])
  final case class ActionPerformed(description: String)
  final case class GetConsensusResponse(response: Boolean)

  def apply(): Behavior[Command] = registry(Map.empty)

  private def registry(store: Map[Int, Pair]): Behavior[Command] =
    Behaviors.receiveMessage {
      case GetStore(replyTo) =>
        replyTo ! Store(store.values.toSeq)
        Behaviors.same
      case CreatePair(key, pair, replyTo) =>
        replyTo ! ActionPerformed(s"Pair ${pair.key} with value=${pair.value} created.")
        registry(store.updated(key, pair))
      case GetPair(key, replyTo) =>
        replyTo ! GetUserResponse(store.get(key))
//        replyTo ! GetUserResponse(Some(Pair(1,1)))
        Behaviors.same
      case InvokeConsensus(txn, replyTo) => {
        val getLocks: ArrayBuffer[Boolean] = ArrayBuffer.empty
        txn.txn.map(element => {
          println("element key", element.key)
          val value = store.get(element.key) match {
            case Some(Pair(_, _, lock)) => lock.tryLock()
            case _ => true
          }
          getLocks += value
        })

        if(getLocks.contains(false)) replyTo ! GetConsensusResponse(false)
        replyTo ! GetConsensusResponse(true)
        Behaviors.same
      }
    }
}
