var j = jQuery.noConflict();

/**
 * 获取浏览器语言类型
 * @return {string} 浏览器国家语言
 */
var getNavLanguage = function() {
	if(navigator.appName == "Netscape") {
		var navLanguage = navigator.language || navigator.userLanguage;
		return navLanguage.substr(0, 2);
	}
	return false;
}
var transfer = function (i18nLanguage) {
	// console.log(j.i18n)
	// debugger
	if(j.i18n == undefined) {
		return false;
	};
	/*
	这里需要进行i18n的翻译
	 */
	//      i18nLanguage="zh_CN";
	//      i18nLanguage="en_US";
	j.i18n.properties({
		name: "js", //资源文件名称
		path: './static/js/i18n/', //资源文件路径
		mode: 'map', //用Map的方式使用资源文件中的值
		language: i18nLanguage,
		callback: function() { //加载成功后设置显示内容
			var insertEle = j(".i18n");
			insertEle.each(function() {
				var contrastName = j(this).attr('contrastName');
				// 根据i18n元素的 contrastName 获取内容写入'
				console.log(j.i18n.prop(contrastName));
				// debugger
				if(contrastName) {
					j(this).html(j.i18n.prop(contrastName));
				};
			});
			// var insertEle_Single = j(".i18n-single")
			// insertEle_Single.each(function() {
			// 	this.path='../static/js/i18n/';
			// 	var contrastName = j(this).attr('contrastName');
			// 	// 根据i18n元素的 contrastName 获取内容写入'
			// 	console.log(j.i18n.prop(contrastName));
			// 	console.log(this.path);
			// 	debugger
			// 	if(contrastName) {
			// 		j(this).html(j.i18n.prop(contrastName));
			// 	};
			// 	this.path='./static/js/i18n/';
			// });
			var insertInputEle = j(".i18n-input");
			insertInputEle.each(function() {
				var selectAttr = j(this).attr('selectattr');
				if(!selectAttr) {
					selectAttr = "value";
				};
				j(this).attr(selectAttr, j.i18n.prop(j(this).attr('contrastName')));
			});
		}
	});
	// debugger
}
/**
 * 设置语言类型： 默认为中文
 */
var i18nLanguage;
var str = document.cookie;
var Language = true;
var strr = str.split("=")
if(strr[0] == 'i18nLanguage')
{
	// debugger
	i18nLanguage = strr[1];
	if(strr[1] == 'zh_CN') Language = false;
}
else i18nLanguage = "en_US";
/*
设置一下网站支持的语言种类
 */
var webLanguage = ['zh_CN', 'en_US'];
/**
 * 执行页面i18n方法
 * @return
 */
var execI18n = function() {
	debugger
	if(!Language) {
		var lang = "en_US"
		document.cookie = "i18nLanguage="+escape("en_US");
		i18nLanguage = "en_US";
		Language = true;
	}
	else {
		debugger
		var lang = "zh_CN"
		document.cookie = "i18nLanguage="+escape("zh_CN");
		i18nLanguage = "zh_CN";
		Language = false;
	}
	/* 需要引入 i18n 文件*/
	transfer(i18nLanguage);
	$.post('/api/check_lang',{lang: lang
        }).done(function (response) {
            let server_code = response['returnValue']
            if (server_code == 1) {
            // success set done
				location.reload();
            }else {
            }
       }).fail(function (){
            console.log("Fail reset");
    })
};
var jump = function () {
	debugger
	transfer(i18nLanguage);
}
// }
/**
 * 单独获取prop
 * @return
 */
var execI18nProp = function(contrastName) {
	var contrastValue = "";
	/* 需要引入 i18n 文件*/
	if(j.i18n == undefined) {
		return false;
	};
	if(contrastName) {
		contrastValue = j.i18n.prop(contrastName);
	};
	return contrastValue
}
