db.events.aggregate([
//    {$limit: 10000},
//    {$project: {"type": true, "count": 1}}
    {$group: {_id: "$type", "count": {$sum: 1}}},
])
.forEach(printjsononeline)
