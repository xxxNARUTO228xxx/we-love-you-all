"use strict";(globalThis["webpackChunkwheel_stamp"]=globalThis["webpackChunkwheel_stamp"]||[]).push([[213],{9085:(e,t,s)=>{s.d(t,{h:()=>i});var a=s(2502);s(3681);const i=(0,a.Q_)("main",{state:()=>({errorMessage:"",okMessage:""})})},3629:(e,t,s)=>{s.d(t,{V:()=>l});s(702),s(4641),s(3269);var a=s(2502),i=s(3681),o=s(9085),r=s(2417);let n="";const l=(0,a.Q_)("model",{state:()=>({loading:!1,load_progress:!1,progress:0,stream_loading:!1,stream_status:!1,images:[],video_images:[],download_url:"",client_id:(0,r.createUID)()}),actions:{async stopStreaming(e){const t=(0,o.h)();try{const s={query:e},a=await i.api.get("/model/rtsp_stop",{query:s});let{items:o}=a;this.stream_status=!1,t.errorMessage=""}catch(s){return console.log("ERROR",s),console.dir(s),t.errorMessage=s.message,s}},async downloadImage(e){const t=(0,o.h)();try{const s=await fetch(`${i.API_ROOT}/model/get_image?filename=${e}`,{method:"GET"}),a=await s.blob(),o=URL.createObjectURL(a);return t.errorMessage="",o}catch(s){return console.log("ERROR",s),console.dir(s),t.errorMessage=s.message,s}},async sendURL(e){console.log(e);const t=(0,o.h)();try{this.stream_loading=!0;const s={rtsp_url:e},a=await i.api.get("/model/rtsp",{query:s});let{items:o}=a;this.stream_status=!0,t.errorMessage=""}catch(s){return console.log("ERROR",s),console.dir(s),t.errorMessage=s.message,s}},async getData(e){const t=(0,o.h)();try{console.log(e),this.loading=!0,this.load_progress=!0;const s=new FormData;s.append("file",e);const a=await fetch(`${i.API_ROOT}/model/archive`,{method:"POST",body:s});if(t.errorMessage="",a.ok){const e=await a.blob(),t=URL.createObjectURL(e);this.download_url=t,this.progress=1,this.load_progress=!1}}catch(s){return console.log("ERROR",s),console.dir(s),t.errorMessage=s.message,s}},takeFrame(){if(""!==n&&void 0!==n)return n},async getFrame(e){n=e},async startConsuming(){console.log("start consuming"),this.ws.connection.onmessage=e=>{let t=JSON.parse(e.data),{event:s,data:a}=t;if("new_frame"==s){let e=a;this.getFrame(e)}if("weapon_detect"==s){let e=a;this.video_images.push(e)}if("video_weapon"==s){let e=a;this.loading=!1,this.images.push(e)}if("progress"==s){let e=a;this.progress=e["progress"]}"reload"==s&&location.reload()}},async sendEcho(){this.ws.sendMessage("echo",{msg:"hello"})}}})},4213:(e,t,s)=>{s.r(t),s.d(t,{default:()=>z});s(702);var a=s(9835),i=s(1957),o=s(6970);const r={class:"container"},n={class:"page-header"},l=["href"],c=(0,a._)("img",{class:"page-header-logo",src:"icons/header-logo.png",width:"50",height:"50",alt:"Логотип FindGun."},null,-1),g=(0,a._)("text",{class:"logo-text"},"FindGun",-1),d=[c,g],m={class:"input-container"},h=["href"],p=["href"],u={class:"main-page"},_=(0,a._)("h1",{class:"visually-hidden"},"Веб-сервис для поиска оружия на видео",-1),w={class:"upload"},f=(0,a._)("h2",{class:"page-title"},"Введите ссылку на RTSP поток",-1),y=(0,a._)("p",{class:"page-subtitle"},"Формат: rtsp://user:password@ip/",-1),b={class:"upload-file__wrapper"},v={class:"upload-button__container container-button"},k={class:"video_board__wrapper"},R={class:"image_board__wrapper"},S={class:"q-pa-md row items-start q-gutter-md"},U={key:0},q={key:0},D=["onClick","src"],I=["src"];function H(e,t,s,c,g,H){const C=(0,a.up)("q-spinner-ball"),V=(0,a.up)("q-inner-loading"),O=(0,a.up)("q-item-label"),T=(0,a.up)("q-item-section"),x=(0,a.up)("q-item"),L=(0,a.up)("q-card"),M=(0,a.up)("q-dialog"),W=(0,a.up)("q-img");return(0,a.wg)(),(0,a.iD)(a.HY,null,[(0,a._)("div",r,[(0,a._)("header",n,[(0,a._)("a",{class:"page-header-logo-link",href:e.getAttUrl()+"/"},d,8,l),(0,a._)("div",m,[(0,a._)("a",{class:"site-link link-header archive",href:e.getAttUrl()+"/"},"Работа с архивом",8,h),(0,a._)("a",{class:"site-link link-header rtsp current-link",href:e.getAttUrl()+"/rtsp"},"Работа с RTSP",8,p)])]),(0,a._)("main",u,[_,(0,a._)("section",w,[f,y,(0,a._)("div",b,[(0,a.wy)((0,a._)("input",{class:"url-input",type:"text",placeholder:"Ссылка","onUpdate:modelValue":t[0]||(t[0]=t=>e.rtspUrl=t)},null,512),[[i.nr,e.rtspUrl]]),(0,a._)("div",v,[(0,a._)("button",{class:"site-button send-button",onClick:t[1]||(t[1]=(...t)=>e.stopStream&&e.stopStream(...t))},"Остановить поток"),(0,a._)("button",{class:"site-button send-button",onClick:t[2]||(t[2]=(...t)=>e.sendURL&&e.sendURL(...t))},"Отправить ссылку")])]),(0,a._)("div",k,[(0,a.Wm)(V,{showing:e.stream_loading,style:{position:"absolute"}},{default:(0,a.w5)((()=>[(0,a.Wm)(C,{size:"100px",color:"dark"})])),_:1},8,["showing"]),(0,a._)("img",{onClick:t[3]||(t[3]=t=>e.showDialogVideo()),id:"stream",style:{height:"100%",width:"100%","border-radius":"8px"}})]),(0,a._)("div",R,[(0,a._)("div",S,[((0,a.wg)(!0),(0,a.iD)(a.HY,null,(0,a.Ko)(e.video_images,(t=>((0,a.wg)(),(0,a.j4)(L,{class:"my-card",key:t.filename},{default:(0,a.w5)((()=>[(0,a.Wm)(x,null,{default:(0,a.w5)((()=>[(0,a.Wm)(T,null,{default:(0,a.w5)((()=>[(0,a.Wm)(O,{class:"card-title"},{default:(0,a.w5)((()=>[(0,a.Uk)((0,o.zw)(t.filename),1)])),_:2},1024),(0,a.Wm)(O,{caption:""},{default:(0,a.w5)((()=>[((0,a.wg)(!0),(0,a.iD)(a.HY,null,(0,a.Ko)(t.class,((s,i)=>((0,a.wg)(),(0,a.iD)(a.HY,{key:i},[(0,a._)("span",{class:(0,o.C_)(e.getClass(s))},(0,o.zw)(s),3),i<t.class.length-1?((0,a.wg)(),(0,a.iD)("span",U,", ")):(0,a.kq)("",!0)],64)))),128))])),_:2},1024),(0,a.Wm)(O,{caption:""},{default:(0,a.w5)((()=>[((0,a.wg)(!0),(0,a.iD)(a.HY,null,(0,a.Ko)(t.poses,((e,s)=>((0,a.wg)(),(0,a.iD)(a.HY,{key:s},[(0,a._)("span",null,(0,o.zw)(e),1),s<t.poses.length-1?((0,a.wg)(),(0,a.iD)("span",q,", ")):(0,a.kq)("",!0)],64)))),128))])),_:2},1024)])),_:2},1024)])),_:2},1024),(0,a._)("img",{onClick:s=>e.showDialog(t),src:"data:image/jpeg;base64,"+t.img},null,8,D)])),_:2},1024)))),128))])])])])]),(0,a.Wm)(M,{modelValue:e.showStream,"onUpdate:modelValue":t[4]||(t[4]=t=>e.showStream=t),"auto-close":"","transition-duration":"300",style:{height:"100%",width:"100%"}},{default:(0,a.w5)((()=>[(0,a._)("section",null,[(0,a._)("img",{src:e.dialogStream,class:"dialog-image",style:{height:"900px","min-width":"1200px"},fit:"scale-up"},null,8,I)])])),_:1},8,["modelValue"]),(0,a.Wm)(M,{modelValue:e.dialog,"onUpdate:modelValue":t[5]||(t[5]=t=>e.dialog=t),"auto-close":"","transition-duration":"300",style:{height:"100%",width:"100%"}},{default:(0,a.w5)((()=>[(0,a.Wm)(W,{src:e.dialogImgSrc,class:"dialog-image",style:{height:"100%","min-width":"1200px","padding-bottom":"0"},fit:"scale-up"},null,8,["src"])])),_:1},8,["modelValue"])],64)}var C=s(499),V=s(3629),O=s(9085),T=s(2502);const x=(0,a.aZ)({name:"IndexPage",setup(){const e=(0,V.V)(),{images:t,stream_loading:s,stream_status:a,video_images:i}=((0,O.h)(),(0,T.Jk)(e));let o=(0,C.iH)(!1),r=(0,C.iH)("Файл не выбран"),n=(0,C.iH)(""),l=(0,C.iH)(!1),c=(0,C.iH)(""),g=(0,C.iH)("");return{showStream:l,video_images:i,encode_frame_cam:c,stream_status:a,rtspUrl:n,file_status:r,images:t,stream_loading:s,store:e,dialog:o,dialogStream:g,img_name:(0,C.iH)(""),img_class:(0,C.iH)("")}},created(){document.title="FindGun | RTSP"},methods:{getClass(e){return"person"===e?"green-text":"weapon"===e?"red-text":""},getAttUrl(){const{protocol:e,hostname:t,port:s,url:a}=window.location;return`${e}//${t}:${s}`},getFrame(){setInterval((()=>{let e=this.store.takeFrame();void 0!==e&&""!==e&&(this.encode_frame_cam=e)}),1)},showDialog:function(e){this.error||(this.img_name=e.filename,this.img_class=e.class.join(", "),this.dialogImgSrc="data:image/jpeg;base64,"+e.img,this.dialog=!0)},showDialogVideo:function(){this.error||(this.showStream=!0)},isValidRTSP(e){return e.startsWith("rtsp://")},async sendURL(){this.isValidRTSP(this.rtspUrl)?(this.store.sendURL(this.rtspUrl),this.store.startConsuming(),this.getFrame()):this.$q.notify({message:"Некорректная RTSP-ссылка!",type:"negative",color:"negative",position:"center",icon:"warning"})},async stopStream(){if(0==this.stream_status)this.$q.notify({message:"Поток еще не запущен!",type:"negative",color:"negative",position:"center",icon:"warning"});else{this.store.stopStreaming("stop"),this.stream_status=!1;document.getElementById("stream");this.encode_frame_cam="",this.$q.notify({message:"Поток остановлен!",type:"info",color:"positive",position:"center",icon:"warning"})}}},watch:{encode_frame_cam(e){if(""!==e){let t="data:image/png;base64,"+e,s=document.getElementById("stream");s.src=t,this.dialogStream=t,this.stream_loading=!1}}}});var L=s(1639),M=s(854),W=s(5304),F=s(4458),P=s(490),Q=s(1233),Z=s(3115),$=s(2899),E=s(335),j=s(9984),A=s.n(j);const Y=(0,L.Z)(x,[["render",H]]),z=Y;A()(x,"components",{QInnerLoading:M.Z,QSpinnerBall:W.Z,QCard:F.Z,QItem:P.Z,QItemSection:Q.Z,QItemLabel:Z.Z,QDialog:$.Z,QImg:E.Z})}}]);