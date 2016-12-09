db.events.aggregate([
        {$match: {"type": "PullRequestEvent", "payload.pull_request.merged": true, "word_diff": {$exists: true}}},
        {$project: {"word_diff": true}},
        {$limit: 500}
    ])
    .map(function(doc) {
        var id = doc._id
            .toString()
            .replace("ObjectId\(\"", "")
            .replace("\"\)", "");
        return {"id": id, "word_diff": doc.word_diff};
    })
    .forEach(function(line) {
        printjsononeline(line);
    })
    ;
