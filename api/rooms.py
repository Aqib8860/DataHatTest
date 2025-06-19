from .models import RoomType, Room, RoomPricing
from bson import ObjectId


# Get Room type name
async def get_room_type_name(db, room_type_id):
    room = await RoomType.get_collection(db).find_one({"_id": ObjectId(room_type_id)}, {"room_type": 1})
    if room:
        return room["room_type"]
    return None


# Get Room number of 
async def get_room_number_of_room(db, room_id):
    room = await Room.get_collection(db).find_one({"_id": ObjectId(room_id)}, {"room_number": 1})
    if room:
        return room["room_number"]
    return None


async def get_property_rooms(db, property_id):
    rooms = await RoomType.get_collection(db).find({"property_id": property_id}).to_list(length=None)
    if rooms:
        for room in rooms:
            room["_id"] = str(room["_id"])
            room["created_at"] = str(room.get("created_at", None))
            room["updated_at"] = str(room.get("updated_at", None))
    
        return rooms
    return []


async def get_rooms_of_room_type(db, room_type_id):
    rooms = await Room.get_collection(db).find({"room_type_id": room_type_id}).to_list(length=None)
    if rooms:
        for room in rooms:
            room["_id"] = str(room["_id"])
            room["created_at"] = str(room.get("created_at", None))
            room["updated_at"] = str(room.get("updated_at", None))
            
        return rooms
    return None


async def get_lowest_room_pricing(db, property_id, available_room_types):
    # Get All Room types of property

    property_room_types = await RoomType.get_collection(db).find({"property_id": property_id}, {"_id": 1}).to_list(length=None)

    if not property_room_types:
        return None

    # Extract IDs into a list
    property_room_type_list = [str(room["_id"]) for room in property_room_types]

    # Compare both list and remove from second if not prensent in first
    filtered_list2 = list(set(available_room_types) & set(property_room_type_list))
    
    # Get room pricing for filtered room types
    room_pricing_cursor = await RoomPricing.get_collection(db).find(
        {"room_type_id": {"$in": filtered_list2}}
    ).to_list(length=None)

    # Extract all prices, excluding "Extra Mattress"
    all_prices = []
    for room in room_pricing_cursor:
        for price_entry in room.get("base_price", []):
            for meal in price_entry.get("meals", []):
                for sharing in meal.get("sharings", []):
                    if sharing["name"] != "Extra Mattress":  # Exclude Extra Mattress
                        all_prices.append(sharing["price"])

    # Return the lowest price if available
    return min(all_prices) if all_prices else None


async def get_room_type_and_lowest_price(db, available_room_types, available_rooms, check_in, check_out, availability):
    # Get All Room types of property
    property_room_types = await RoomType.get_collection(db).find(
        {"_id": {"$in": available_room_types}},
        {"_id": 1, "room_type": 1, "amenities": 1, "images": 1}
    ).to_list(length=None)

    if not property_room_types:
        return None

    # Extract IDs into a list
    property_room_type_list = [str(room["_id"]) for room in property_room_types]

    
    # Get room pricing for filtered room types
    room_pricing_cursor = await RoomPricing.get_collection(db).find(
        {"room_type_id": {"$in": property_room_type_list}}
    ).to_list(length=None)

    # Extract all prices, excluding "Extra Mattress"
    all_prices = []
    for room in room_pricing_cursor:
        for price_entry in room.get("base_price", []):
            for meal in price_entry.get("meals", []):
                for sharing in meal.get("sharings", []):
                    if sharing["name"] != "Extra Mattress":  # Exclude Extra Mattress
                        all_prices.append(sharing["price"])

    # Return the lowest price if available
    min_price = min(all_prices) if all_prices else None

    for room_type in property_room_types:
        
        room_type["_id"] = str(room_type["_id"])
        room_type["available_dates"] = availability[room_type["_id"]]
        
        # get available rooms of room_type
        room_type["available_rooms"] = await Room.get_collection(db).aggregate([
            {
                "$match": {
                    "room_type_id": room_type["_id"],
                    "_id": {"$in": available_rooms}
                }
            },
            {
                "$addFields": {
                    "_id": {"$toString": "$_id"}
                }
            }
        ]).to_list(length=None)

        room_pricing = await RoomPricing.get_collection(db).aggregate([
            {
                "$match": {
                    "room_type_id": room_type["_id"],
                    "base_price": {
                        "$elemMatch": {
                            "start_date": {"$lte": check_out},
                            "end_date": {"$gte": check_in}
                        }
                    }
                }
            },
            {
                "$project": {
                    "base_price": {
                        "$filter": {
                            "input": "$base_price",
                            "as": "bp",
                            "cond": {
                                "$and": [
                                    { "$lte": ["$$bp.start_date", check_out] },
                                    { "$gte": ["$$bp.end_date", check_in] }
                                ]
                            }
                        }
                    },
                }
            },
            {
                "$addFields": {
                    "_id": {"$toString": "$_id"}
                }
            }
        ]).to_list(length=None)
        if room_pricing: 
            room_type["base_price"] = room_pricing[0]["base_price"]
        else: 
            room_type["base_price"] = []


    return property_room_types, min_price


async def get_booked_room_numbers(db, room_type_id, all_rooms):
    room_type_rooms = await Room.get_collection(db).aggregate([
        {
            "$match": {
                "room_type_id": room_type_id, 
                "_id": {"$in": all_rooms}
            }
        }, 
        {
            "$project": {
                "_id": {"$toString": "$_id"},
                "room_number": 1
            }
        },
        ]).to_list(length=None)
    
    return room_type_rooms
    

