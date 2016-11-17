#!/usr/bin/env node

const async = require('asyncawait/async');
const await = require('asyncawait/await');
const diffLineToWord = require('diff-linetoword');
const getStdin = require('get-stdin');
const JsDiff = require('diff');
const mongodb = require('mongodb');
const MongoClient = mongodb.MongoClient;
const ObjectId = mongodb.ObjectId;

const MAX_DIFF_CHAR_COUNT = 100000;

function usage() {
    console.log("node index.js MONGODB_ID < line_diff_contents.diff");
}

if(process.argv.length < 3) {
    console.error("A MongoDB ID is required");
    usage();
    process.exit(2);
}

const mongoID = process.argv[2];
const convertDiffAndUpdateMongo = async(function() {
/* start async */

let line_diff = await(getStdin());
if(line_diff.length > MAX_DIFF_CHAR_COUNT) {
    // Allow it to complete and generate no diff at all to simplify processing.
    line_diff = "";
}

const word_diff = JsDiff.parsePatch(line_diff)
    .map(diffLineToWord)
    .join("\n");

MongoClient.connect('mongodb://localhost:27017/github', function(err, db) {
    if(err != null) {
        console.error("Could not connect to MongoDB");
        process.exit(1);
    }

    let collection = db.collection('events');
    collection.updateOne({"_id": ObjectId(mongoID)}, { "$set": {"word_diff": word_diff}});
    console.log("Successfully updated diff for ID: " + mongoID);

    db.close();
});

/* end async */
});

convertDiffAndUpdateMongo();
