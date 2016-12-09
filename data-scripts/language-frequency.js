db.languages_fixed.aggregate([
    {$group: {_id: {$setIntersection: "$value"}, "count": {$sum: 1}}},
    {$project: {"count": true, "size": {$size: "$_id"}}},
    {$match: {"size": {$gte: 2, $lte: 3}}},
    {$project: {"count": true}},
    {$sort: {"count": -1}},
    {$limit: 20},
])
.forEach(function(doc) {
    printjsononeline(doc);
})

