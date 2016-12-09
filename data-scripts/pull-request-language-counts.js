db.events.aggregate([
    {$match: {"type": "PullRequestEvent", "payload.pull_request.merged": true}},
    {$group: {
        _id: "$payload.pull_request.head.repo.language",
        "count": {$sum: 1},
    }},
])
.forEach(function(doc) {
    printjsononeline(doc);
});
