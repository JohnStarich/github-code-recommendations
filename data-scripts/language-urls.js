db.events.aggregate([
    { $match: {
        type: "PullRequestEvent",
        languages: {$exists: false},
    }},
    {$skip: 15000},
    {$limit: 5000},
    { $project: {
        languages_url: "$payload.pull_request.base.repo.languages_url",
    }},
    {$group: {
        _id: null,
        languages: {$addToSet: "$languages_url"},
    }},
    {$unwind: "$languages"},
]).forEach(function(doc) {
    print(doc.languages);
})

