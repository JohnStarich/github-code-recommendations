db.languages.mapReduce(
    function() {
        var langs = Object.keys(this)
                        .filter((key) => key != '_id')
                        .sort()
                        ;
        emit(this._id, langs);
        /*this.items.forEach(function(doc) {
            print(Object.keys(doc));
        });*/
    },
    function(key, values) {
    },
    {
        out: {
            replace: 'languages_fixed'
        }
    }
)
