db.events.aggregate([
        {$match: {"type": "PullRequestEvent", "word_diff": {$exists: false}}},
        {$project: {"diff_url": "$payload.pull_request.diff_url"}},
        {$limit: 50}
    ])
    .map(function(doc) {
        var id = doc._id
            .toString()
            .replace("ObjectId\(\"", "")
            .replace("\"\)", "");
        return {"id": id, "diff_url": doc.diff_url};
    })
    .forEach(function(line) {
        printjsononeline(line);
    })
    ;
