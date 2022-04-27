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

/**
 * 设置语言类型： 默认为中文
 */
var i18nLanguage = "en_US";
var Language = 1;
/*
设置一下网站支持的语言种类
 */
var webLanguage = ['zh_CN', 'en_US'];
/**
 * 执行页面i18n方法
 * @return
 */
var execI18n = function() {
	if(Language == 0) {
		i18nLanguage = "en_US";
		Language = 1;
	}
	else {
		i18nLanguage = "zh_CN";
		Language = 0;
	}
	// 获取浏览器语言
	// var navLanguage = getNavLanguage();
	// if(navLanguage) {
	// 	// 判断是否在网站支持语言数组里
	// 	var charSize = $.inArray(navLanguage, webLanguage);
	// 	if(charSize > -1) {
	// 		i18nLanguage = navLanguage;
	// 	};
	// } else {
	// 	console.log("not navigator");
	// 	return false;
	// }
	/* 需要引入 i18n 文件*/
	if($.i18n == undefined) {
		return false;
	};
	/*
	这里需要进行i18n的翻译
	 */
	//      i18nLanguage="zh_CN";
	//      i18nLanguage="en_US";
	$.i18n.properties({
		name: "js", //资源文件名称
		path: './static/js/i18n/', //资源文件路径
		mode: 'map', //用Map的方式使用资源文件中的值
		language: i18nLanguage,
		callback: function() { //加载成功后设置显示内容
			console.log(i18nLanguage);
			var insertEle = $(".i18n");
			insertEle.each(function() {
				//筛去其中的html语法
				// var html = $(this).html();
				// var reg = /<(.*)>/;
				// if (reg.test(html)) {
				// 	var htmlValue = reg.exec(html)[0];
				// 	$(this).html(htmlValue + $.i18n.prop(contrastName));
				// }
				var contrastName = $(this).attr('contrastName');
				// 根据i18n元素的 contrastName 获取内容写入'
				console.log($.i18n.prop(contrastName));
				// debugger
				if(contrastName) {
					$(this).html($.i18n.prop(contrastName));
				};
			});
			var insertInputEle = $(".i18n-input");
			insertInputEle.each(function() {
				var selectAttr = $(this).attr('selectattr');
				if(!selectAttr) {
					selectAttr = "value";
				};
				$(this).attr(selectAttr, $.i18n.prop($(this).attr('contrastName')));
			});
		}
	});
};
/**
 * 单独获取prop
 * @return
 */
var execI18nProp = function(contrastName) {
	var contrastValue = "";
	/* 需要引入 i18n 文件*/
	if($.i18n == undefined) {
		return false;
	};
	if(contrastName) {
		contrastValue = $.i18n.prop(contrastName);
	};
	return contrastValue
}