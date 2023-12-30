package com.example

import com.example.UserRegistry.ActionPerformed

import spray.json.RootJsonFormat
import spray.json.DefaultJsonProtocol

object JsonFormats  {
  // import the default encoders for primitive types (Int, String, Lists etc)
  import DefaultJsonProtocol._

  implicit val pairJsonFormat: RootJsonFormat[Pair] = jsonFormat2(Pair.apply)
  implicit val storeJsonFormat: RootJsonFormat[Store] = jsonFormat1(Store.apply)

  implicit val actionPerformedJsonFormat: RootJsonFormat[ActionPerformed]  = jsonFormat1(ActionPerformed.apply)
}
