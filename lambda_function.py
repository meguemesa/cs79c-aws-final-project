
import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("biomed-antibody-repository")


def reply(status, data):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(data, default=str)
    }


def lambda_handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method")
    method = method or event.get("httpMethod") or "GET"

    try:
        if method == "GET":
            items = []
            response = table.scan()
            items.extend(response.get("Items", []))

            while "LastEvaluatedKey" in response:
                response = table.scan(
                    ExclusiveStartKey=response["LastEvaluatedKey"]
                )
                items.extend(response.get("Items", []))

            return reply(200, items)

        body = event.get("body", {})
        if isinstance(body, str):
            body = json.loads(body)

        if not isinstance(body, dict):
            return reply(400, {"error": "Body must be a JSON object"})

        if method == "POST":
            required = [
                "antibodyID", "antibodyName", "clone",
                "fluorophore", "quantityRemaining"
            ]
            if any(field not in body for field in required):
                return reply(400, {"error": "Missing required fields"})

            try:
                quantity = Decimal(str(body["quantityRemaining"]))
                if not quantity.is_finite() or quantity < 0:
                    raise ValueError()
            except (ValueError, TypeError):
                return reply(400, {"error": "Invalid quantity"})

            item = {
                "antibodyID": str(body["antibodyID"]),
                "antibodyName": str(body["antibodyName"]),
                "clone": str(body["clone"]),
                "fluorophore": str(body["fluorophore"]),
                "quantityRemaining": quantity
            }

            try:
                table.put_item(
                    Item=item,
                    ConditionExpression="attribute_not_exists(antibodyID)"
                )
            except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
                return reply(409, {"error": "Antibody ID already exists"})

            return reply(201, {
                "message": "Antibody added",
                "item": item
            })

        if method == "PUT":
            antibody_id = body.get("antibodyID")
            if not antibody_id or "quantityRemaining" not in body:
                return reply(400, {"error": "ID and quantity required"})

            try:
                quantity = Decimal(str(body["quantityRemaining"]))
                if not quantity.is_finite() or quantity < 0:
                    raise ValueError()
            except (ValueError, TypeError):
                return reply(400, {"error": "Invalid quantity"})

            try:
                response = table.update_item(
                    Key={"antibodyID": antibody_id},
                    UpdateExpression="SET quantityRemaining = :q",
                    ConditionExpression="attribute_exists(antibodyID)",
                    ExpressionAttributeValues={":q": quantity},
                    ReturnValues="ALL_NEW"
                )
            except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
                return reply(404, {"error": "Antibody not found"})

            return reply(200, {
                "message": "Quantity updated",
                "item": response["Attributes"]
            })

        return reply(405, {"error": "Method not allowed"})

    except (ValueError, TypeError, json.JSONDecodeError):
        return reply(400, {"error": "Invalid request data"})
