package com.example

import akka.actor.typed.ActorRef
import akka.actor.typed.Behavior
import akka.actor.typed.scaladsl.Behaviors

import scala.collection.immutable
import java.util.concurrent.locks.Lock
import scala.None
import spray.json._

final case class Pair(key: String, value: Int, lock: Lock)
final case class Store(pairs: immutable.Seq[Pair])
final case class Txn(txn: List[Pair])

object UserRegistry {
  sealed trait Command
  final case class GetStore(replyTo: ActorRef[Store]) extends Command
  final case class CreatePair(pair: Pair, replyTo: ActorRef[ActionPerformed]) extends Command
  final case class GetPair(key: String, replyTo: ActorRef[GetUserResponse]) extends Command
  final case class InvokeConsensus(key: String, replyTo: ActorRef[GetConsensusResponse]) extends Command
//  final case class DeleteUser(name: String, replyTo: ActorRef[ActionPerformed]) extends Command

  final case class GetUserResponse(maybePair: Option[Pair])
  final case class ActionPerformed(description: String)
  final case class GetConsensusResponse(response: Boolean)

  def apply(): Behavior[Command] = registry(Map.empty)

  private def registry(store: Map[String, Pair]): Behavior[Command] =
    Behaviors.receiveMessage {
      case GetStore(replyTo) =>
        replyTo ! Store(store.values.toSeq)
        Behaviors.same
      case CreatePair(pair, replyTo) =>
        replyTo ! ActionPerformed(s"Pair ${pair.key} with value=${pair.value} created.")
        registry(store.updated(pair.key, pair))
      case GetPair(key, replyTo) =>
        replyTo ! GetUserResponse(store.get(key))
        Behaviors.same
      case InvokeConsensus(key, replyTo) => {
        val value = store.get(key) match {
          case Some(Pair(_, _, lock)) => GetConsensusResponse(lock.tryLock())
          case _ => GetConsensusResponse(true)
        }
        replyTo ! value
        Behaviors.same
      }
    }
}
