package com.example

import com.example.UserRegistry.{ActionPerformed, GetConsensusResponse}
import spray.json.DefaultJsonProtocol


object JsonFormats  {
  // import the default encoders for primitive types (Int, String, Lists etc)
  import DefaultJsonProtocol._
  import spray.json._

  import java.util.concurrent.locks.Lock

  implicit val reentrantLockFormat: JsonFormat[Lock] = new JsonFormat[Lock] {
    override def write(obj: Lock): JsValue = JsString("Lock")
    override def read(json: JsValue): Lock = throw new UnsupportedOperationException("Deserialization of Lock not supported")
  }
  implicit val pairJsonFormat: RootJsonFormat[Pair] = jsonFormat3(Pair.apply)
  implicit val storeJsonFormat: RootJsonFormat[Store] = jsonFormat1(Store.apply)
  implicit val booleanJsonFormat: RootJsonFormat[GetConsensusResponse] = jsonFormat1(GetConsensusResponse.apply)
  implicit val actionPerformedJsonFormat: RootJsonFormat[ActionPerformed]  = jsonFormat1(ActionPerformed.apply)
  implicit val keyValueJsonFormat: RootJsonFormat[KeyValue] = jsonFormat3(KeyValue.apply)
  implicit val txnJsonFormat: RootJsonFormat[Txn] = jsonFormat1(Txn.apply)
}
