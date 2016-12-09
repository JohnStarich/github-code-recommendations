db.events.aggregate([
        {$match: {"type": "PullRequestEvent"}},
        {$project: {_id: false, "language_url": "$payload.pull_request.base.repo.languages_url"}},
        {$sort: {"language_url": 1}},
        {$group: {_id: null, lastLanguage: {$addToSet: "$language_url"}}},
        {$unwind: "$lastLanguage"},
    ])
    .forEach(function(line) {
        printjsononeline(line);
    })
    ;
