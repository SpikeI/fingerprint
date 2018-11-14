(function (){
    $(function() {

        // promise works

        function start(resolve, reject) {
            resolve();
        }

        function do_cross_work() {
            return new Promise(function (resolve, reject) {
                var loader;
                loader = new Loader(resolve, reject);
            })
        }

        function do_check_storage_work(){
            return new Promise(check_storage);
        }

        function detect_ip_address(){
            return new Promise(function (resolve, reject){
                local_ipaddr = ""
                getIPs(function(ip){
                    console.log('')
                    local_ipaddr = ip;
                    resolve(true);
                })
            })
        }


        function finish_work(result){
            getIPs(function(ip){
                console.log("[+] Get IP:");
                console.log(ip);
            });
            if(result === "[check storage failed]"){
                console.log("[-] Error in check storage");
            }else if(result === "[storage network error]"){
                console.log("[-] storage network error");
            }else if(result === "[storage finished]"){
                // found identify
                console.log('[+] Get id from storage');
                window.location.href = "/service"
            }else if(result === "[Finish collect data]"){
                // found / create a identify
                console.log('[+] finish from fingerprint');
                $("#status").html("Finish Fingerprinting");
                $("#test_canvases")[0].hidden = true;
                $("#ask_panel")[0].hidden = false;

            }else{
                console.log('[-] some thing error')
            }
            // console.log("[+] Finished get out from " + result);
        }

        // promise chains

        var p = new Promise(start);
        p.then(do_check_storage_work).then(detect_ip_address).then(do_cross_work)
            .then(finish_work).catch(finish_work);
    });
})();
