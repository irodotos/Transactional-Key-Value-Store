package com.example

import akka.actor.typed.ActorRef
import akka.actor.typed.Behavior
import akka.actor.typed.scaladsl.Behaviors
import scala.collection.immutable

final case class Pair(key: String, value: Int)
final case class Store(pairs: immutable.Seq[Pair])

object UserRegistry {
  sealed trait Command
  final case class GetStore(replyTo: ActorRef[Store]) extends Command
  final case class CreatePair(pair: Pair, replyTo: ActorRef[ActionPerformed]) extends Command
  final case class GetPair(key: String, replyTo: ActorRef[GetUserResponse]) extends Command
//  final case class DeleteUser(name: String, replyTo: ActorRef[ActionPerformed]) extends Command

  final case class GetUserResponse(maybePair: Option[Pair])
  final case class ActionPerformed(description: String)

  def apply(): Behavior[Command] = registry(Set.empty)

  private def registry(store: Set[Pair]): Behavior[Command] =
    Behaviors.receiveMessage {
      case GetStore(replyTo) =>
        replyTo ! Store(store.toSeq)
        Behaviors.same
      case CreatePair(pair, replyTo) =>
        replyTo ! ActionPerformed(s"Pair ${pair.key} with value=${pair.value} created.")
        registry(store + pair)
      case GetPair(key, replyTo) =>
        replyTo ! GetUserResponse(store.find(_.key == key))
        Behaviors.same
//      case DeleteUser(name, replyTo) =>
//        replyTo ! ActionPerformed(s"User $name deleted.")
//        registry(users.filterNot(_.name == name))
    }
}
