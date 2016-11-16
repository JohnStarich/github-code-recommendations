const diffLineToWord = require('diff-linetoword');
const getStdin = require('get-stdin');
const JsDiff = require('diff');

getStdin().then(function(line_diff) {
    if(line_diff.length > 5000) {
        process.exit(1);
    }
    const patches = JsDiff.parsePatch(line_diff);
    patches.map(diffLineToWord)
        .forEach(function(patch) {
            console.log(patch);
        });
});
