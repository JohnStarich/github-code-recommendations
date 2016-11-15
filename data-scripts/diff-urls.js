var cursor = db.events.aggregate([
    {$match: {"type": "PullRequestEvent"}},
    {$project: {"diff_url": "$payload.pull_request.diff_url"}},
    {$limit: 100}
]);
while(cursor.hasNext()) {
    printjsononeline(cursor.next());
}
