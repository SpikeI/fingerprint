
    function check_storage(parent_resolve, parent_reject){
        // session
        session_mark = "";
        session_mark = window.sessionStorage.getItem("SpikeMark");

        // localstorage
        local_mark = "";
        local_mark = window.localStorage.getItem("SpikeMark");

        // web sql
        websql_mark = "";
        function get_websql(promise_return){
            return new Promise(function (resolve, reject){

                // firefox doesn't support websql
                let ua = navigator.userAgent.toLowerCase();
                if(ua.match(/firefox\/([\d.]+)/)){
                    websql_mark = ""
                    resolve(true)
                }else{
                    let db = openDatabase('mydb', '1.0', 'Test', 2 * 1024 * 1024);
                    db.transaction(function (tx) {
                       tx.executeSql('SELECT * FROM SPIKE', [], function (tx, results) {
                          var len = results.rows.length;
                          if(len > 0) {
                              websql_mark = results.rows.item(0)['mark'];
                          }else{
                              websql_mark = "";
                          }
                          resolve(true);
                       }, function(error){
                           websql_mark = "";
                           resolve(true);
                       });
                    });
                }


            })
        }


        // index DB
        indexDB_mark = "";

        function get_indexedDB(promise_return){
            return new Promise(function (resolve, reject) {
                if("indexedDB" in window) {
                    let request = indexedDB.open("SpikeMark");
                    request.onsuccess = function (event) {
                        db = request.result;
                        // console.log(db);
                        // console.log(db.objectStoreNames);
                        if(db.objectStoreNames.contains('Spike')){
                            let transaction = db.transaction(['Spike']);
                            let objectStore = transaction.objectStore('Spike');
                            let res = objectStore.get("SpikeMark");
                            // console.log(objectStore.count())
                            res.onerror = function (event) {
                                resolve(false);
                            };
                            res.onsuccess = function (event) {
                                console.log(res.result['value']);
                                if(res.result){
                                    indexDB_mark = res.result['value'];
                                    resolve(true);
                                }
                            }
                        }else{
                            indexDB_mark = "";
                            resolve(false);
                        }
                    };
                    request.onerror = function(){
                        indexDB_mark = "";
                        resolve(false)
                    }
                }
            })
        }

        function check_mark(promise_return) {
            console.log("[+] Get Session mark");
            console.log(session_mark);
            console.log("[+] Get local mark");
            console.log(local_mark);
            console.log("[+] Get websql mark");
            console.log(websql_mark);
            console.log("[+] Get indexdb mark");
            console.log(indexDB_mark);

            // if(!promise_return){
            //     parent_reject("[check storage failed]");
            // }

            // post to server to check idnetify
            let post_msg = {};
            post_msg['session_mark'] = session_mark;
            post_msg['local_mark'] = local_mark;
            post_msg['websql_mark'] = websql_mark;
            post_msg['indexDB_mark'] = indexDB_mark;

            $.post("/fingerprint/check_storage",
                post_msg,
                function(data, status){
                    server_res = JSON.parse(data);
                    if(server_res.status === "valid"){
                        // found storage in database
                        set_storage(server_res.mark);
                        parent_reject("[storage finished]");
                    }else{
                        parent_resolve();
                    }
                }).error(function(){
                    parent_reject("[storage network error]");
                })

        }

        s = new Promise(function (resolve, reject) {
            resolve(true);
        });
        s.then(get_websql).then(get_indexedDB).then(check_mark).catch(function (result) {
            console.log('[-] Can not get here');
        })
    }


    function set_storage(mark){

        console.log('[1] Start set storge');

        // 1 session storage
        window.sessionStorage.setItem("SpikeMark", mark);
        console.log("[2] Set Session Storage");

        // 2 local storage
        window.localStorage.setItem("SpikeMark", mark);
        console.log("[3] Set local Storage");

        // 3 web sql
        let ua = navigator.userAgent.toLowerCase();
        if(ua.match(/firefox\/([\d.]+)/)){
            console.log("[-] Firefox doesnt support websql");
        }else{
            let db = openDatabase('mydb', '1.0', 'Test', 2 * 1024 * 1024);
            db.transaction(function (tx) {
                tx.executeSql('DROP TABLE IF EXISTS SPIKE');
                tx.executeSql('CREATE TABLE IF NOT EXISTS SPIKE (id unique, mark)');
                tx.executeSql('INSERT INTO SPIKE (id, mark) VALUES (1, "'+ mark +'")');
            });
            console.log("[4] Set websql mark");
        }


        // 4 indexedDB
        let request = indexedDB.open("SpikeMark");
        request.onupgradeneeded = function() {
            let db = request.result;
            let store = db.createObjectStore("Spike", {keyPath: "id"});
            store.createIndex("value", "value");
            store.put({id: "SpikeMark", value: mark});
        };
        // request.onsuccess = function () {
        //     let db = request.result;
        //     let spike = db.transaction(['Spike'], "readwrite").objectStore("Spike");
        //     spike.delete("SpikeMark");
        //     spike.add({id:"SpikeMark", value: mark})
        // }
    }



