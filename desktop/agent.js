'use strict'

if (Java.available) {
	Java.perform(function() {
		console.log("[*] Script Started")
		const MethodCall = Java.use("io.flutter.plugin.common.MethodCall");
		const FileOutputStream = Java.use("java.io.FileOutputStream");
		const filename = "/data/user/0/com.bendingspoons.live.quiz/log.json";
		const StringClass = Java.use("java.lang.String");

		function save(data){
                  var fos = FileOutputStream.$new(filename);
			try{
				var s = StringClass.$new(data);
				var count=0;
				do{
					var j = s.indexOf('\\"');
					if (j > 0){
						s = s.substring(0,j)+"'"+s.substring(j+2);
					}
				}while(j > 0);
                                var ss = StringClass.$new(s);
				fos.write(ss.getBytes());
			} catch(e){
				console.error(e);
			}
			return;
		}

		MethodCall.argument.implementation = function(key){
			var ret = this.argument(key);
			if (key == "string"){
				save(ret);
                        }
			return ret;
		}

	});
}
