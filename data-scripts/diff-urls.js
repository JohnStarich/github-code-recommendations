db.events.aggregate([
        {$match: {
            "type": "PullRequestEvent",
            "payload.pull_request.merged": true,
            "word_diff": "",
            "payload.pull_request.head.repo.language": "Python",
        }},
        {$project: {"diff_url": "$payload.pull_request.diff_url"}},
        {$limit: 500}
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
