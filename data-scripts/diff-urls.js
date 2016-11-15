db.events.aggregate([
        {$match: {"type": "PullRequestEvent"}},
        {$project: {"diff_url": "$payload.pull_request.diff_url"}},
        {$limit: 50}
    ])
    .map(function(doc) {
        var id = doc._id
            .toString()
            .replace("ObjectId\(\"", "")
            .replace("\"\)", "");
        var newDoc = {};
        newDoc[id] = doc.diff_url;
        return newDoc;
    })
    .forEach(function(line) {
        printjsononeline(line);
    })
    ;
