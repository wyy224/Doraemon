var sEO={
    $:function(exp){//获取对象（1个、多个）
        var el;
        if (/^#\w+$/.test(exp)){
            el=document.querySelector(exp);
        } else {
            el=document.querySelectorAll(exp);
        }
        return el;
    },
    e:function (ev) {
        return ev||event;
    },
    getType:function () {
        return this.e().type()
    },
    getTarget:function () {
        return this.e().target||this.e().srcElement;
    },
    stopBubble:function () {//阻止时间冒泡
        if (this.e().stopPropagation)
            this.e().stopPropagation();
        else
            this.e().cancelBubble=true;
    },
    stopDefault:function () {//阻止默认事件
        if (this.e().preventDefault)
            this.e().preventDefault();
        else
            this.e().returnValue=false;
    },
    addEvent:function (el,type,fn) {//添加事件
        /*el：对象，type：事件名称,fn：回调函数*/
        if (el.addEventListener)
            el.addEventListener(type,fn,false);
        else if (el.attachEvent)
            el.attachEvent(type,fn);
        else
            el['on'+type]=fn;
    },
    delEvent:function (el,type,fn) {//删除事件
        /*el：对象，type：事件名称,fn：回调函数*/
        if (el.addEventListener)
            el.removeEventListener(type,fn,false);
        else if (el.attachEvent)
            el.detachEvent(type,fn);
        else
            el['on'+type]=null;
    },
    agent:function (parent,targetName,type,fun) {//单个事件代理
        //代理对象（1个），被代理的对象，事件名，回调函数
        this.addEvent(parent,type,function (ev) {
            var e=ev||event;
            var target=e.target||e.srcElement;
            while (target.nodeName!==targetName.toUpperCase() && target!==parent){
                target=target.parentNode;
            }
            if (target.nodeName===targetName.toUpperCase())
                fun.call(target);//将回调函数作用给target对象
        })
    },
    agents:function (parent,targetArr,type,fun) {//多个事件代理
        //代理对象（多个），被代理的对象，事件名，回调函数
        var _this=this;
        targetArr.forEach(function (el) {
            _this.addEvent(parent,type,function (ev) {
                var e=ev||event;
                var target=e.target||e.srcElement;
                while (target.nodeName!==el.toUpperCase() && target!==parent){
                    target=target.parentNode;
                }
                if (target.nodeName===el.toUpperCase())
                    fun.call(target);
            })
        })
    },
    getScroll:function (el) {//滚动条滚动
        var top=0,left=0;
        if (el===document){
            left=el.body.scrollLeft||el.documentElement.scrollLeft;
            top=el.body.scrollTop||el.documentElement.scrollTop;
        }else{
            left=el.scrollLeft;
            top=el.screenTop;
        }
        return {left:left,top:top}
    },
    getCookie:function (key) {
        var ck=document.cookie;
        var arr=ck.split('; ');
        for (var i in arr){
            var temp=arr[i].split('=');
            if (temp[0]===key)
                return temp[1];
        }
        return '';
    },
    setCookie:function (key,value,iDate) {
        var d=new Date();
        d.setDate(d.getDate()+iDate);
        document.cookie =`${key}=${value};expires=${d}`
    },
    removeCookie:function (key) {
        this.setCookie(key,0,-1);
    },
    clearClass:function (cArr,cls) {//清除class
        //对象数组，class名字
        // for (var i=0;i<cArr.length;i++){
        //     if (cArr[i].classList.contains(cls)){
        //         cArr[i].classList.remove(cls);
        //         break;
        //     }
        // }
       [].forEach.call(cArr,function (el) {
           if (el.classList.contains(cls)){
               el.classList.remove(cls);
               return false;
           }
       });
    },
    getPos:function (el){
        var left=el.offsetLeft;
        var top=el.offsetTop;
        while(el===el.offsetParent){
            left+=el.offsetLeft;
            top+=el.offsetTop;
        }
        return {left:left,top:top}
    }
};