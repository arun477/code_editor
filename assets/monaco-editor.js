"use strict";var define,AMDLoader,_amdLoaderGlobal=this,_commonjsGlobal="object"==typeof global?global:{};!function(e){function t(){this._detected=!1,this._isWindows=!1,this._isNode=!1,this._isElectronRenderer=!1,this._isWebWorker=!1,this._isElectronNodeIntegrationWebWorker=!1}e.global=_amdLoaderGlobal,Object.defineProperty(t.prototype,"isWindows",{get:function(){return this._detect(),this._isWindows},enumerable:!1,configurable:!0}),Object.defineProperty(t.prototype,"isNode",{get:function(){return this._detect(),this._isNode},enumerable:!1,configurable:!0}),Object.defineProperty(t.prototype,"isElectronRenderer",{get:function(){return this._detect(),this._isElectronRenderer},enumerable:!1,configurable:!0}),Object.defineProperty(t.prototype,"isWebWorker",{get:function(){return this._detect(),this._isWebWorker},enumerable:!1,configurable:!0}),Object.defineProperty(t.prototype,"isElectronNodeIntegrationWebWorker",{get:function(){return this._detect(),this._isElectronNodeIntegrationWebWorker},enumerable:!1,configurable:!0}),t.prototype._detect=function(){this._detected||(this._detected=!0,this._isWindows=t._isWindows(),this._isNode=typeof module<"u"&&!!module.exports,this._isElectronRenderer=typeof process<"u"&&typeof process.versions<"u"&&typeof process.versions.electron<"u"&&"renderer"===process.type,this._isWebWorker="function"==typeof e.global.importScripts,this._isElectronNodeIntegrationWebWorker=this._isWebWorker&&typeof process<"u"&&typeof process.versions<"u"&&typeof process.versions.electron<"u"&&"worker"===process.type)},t._isWindows=function(){return!!(typeof navigator<"u"&&navigator.userAgent&&0<=navigator.userAgent.indexOf("Windows"))||typeof process<"u"&&"win32"===process.platform},e.Environment=t}(AMDLoader=AMDLoader||{}),function(r){var o=function(e,t,r){this.type=e,this.detail=t,this.timestamp=r},e=(r.LoaderEvent=o,t.prototype.record=function(e,t){this._events.push(new o(e,t,r.Utilities.getHighPerformanceTimestamp()))},t.prototype.getEvents=function(){return this._events},t);function t(e){this._events=[new o(1,"",e)]}function n(){}r.LoaderEventRecorder=e,n.prototype.record=function(e,t){},n.prototype.getEvents=function(){return[]},n.INSTANCE=new n,r.NullLoaderEventRecorder=n}(AMDLoader=AMDLoader||{}),function(e){function o(){}o.fileUriToFilePath=function(e,t){if(t=decodeURI(t).replace(/%23/g,"#"),e){if(/^file:\/\/\//.test(t))return t.substr(8);if(/^file:\/\//.test(t))return t.substr(5)}else if(/^file:\/\//.test(t))return t.substr(7);return t},o.startsWith=function(e,t){return e.length>=t.length&&e.substr(0,t.length)===t},o.endsWith=function(e,t){return e.length>=t.length&&e.substr(e.length-t.length)===t},o.containsQueryString=function(e){return/^[^\#]*\?/gi.test(e)},o.isAbsolutePath=function(e){return/^((http:\/\/)|(https:\/\/)|(file:\/\/)|(\/))/.test(e)},o.forEachProperty=function(e,t){if(e){var r=void 0;for(r in e)e.hasOwnProperty(r)&&t(r,e[r])}},o.isEmpty=function(e){var t=!0;return o.forEachProperty(e,function(){t=!1}),t},o.recursiveClone=function(e){if(!e||"object"!=typeof e||e instanceof RegExp||!Array.isArray(e)&&Object.getPrototypeOf(e)!==Object.prototype)return e;var r=Array.isArray(e)?[]:{};return o.forEachProperty(e,function(e,t){r[e]=t&&"object"==typeof t?o.recursiveClone(t):t}),r},o.generateAnonymousModule=function(){return"===anonymous"+o.NEXT_ANONYMOUS_ID+++"==="},o.isAnonymousModule=function(e){return o.startsWith(e,"===anonymous")},o.getHighPerformanceTimestamp=function(){return this.PERFORMANCE_NOW_PROBED||(this.PERFORMANCE_NOW_PROBED=!0,this.HAS_PERFORMANCE_NOW=e.global.performance&&"function"==typeof e.global.performance.now),(this.HAS_PERFORMANCE_NOW?e.global.performance:Date).now()},o.NEXT_ANONYMOUS_ID=1,o.PERFORMANCE_NOW_PROBED=!1,o.HAS_PERFORMANCE_NOW=!1,e.Utilities=o}(AMDLoader=AMDLoader||{}),function(u){function r(e){if(e instanceof Error)return e;var t=new Error(e.message||String(e)||"Unknown Error");return e.stack&&(t.stack=e.stack),t}u.ensureError=r;n.validateConfigurationOptions=function(e){var t;return"string"!=typeof(e=e||{}).baseUrl&&(e.baseUrl=""),"boolean"!=typeof e.isBuild&&(e.isBuild=!1),"object"!=typeof e.paths&&(e.paths={}),"object"!=typeof e.config&&(e.config={}),"u"<typeof e.catchError&&(e.catchError=!1),"u"<typeof e.recordStats&&(e.recordStats=!1),"string"!=typeof e.urlArgs&&(e.urlArgs=""),"function"!=typeof e.onError&&(e.onError=function(e){if("loading"===e.phase)return console.error('Loading "'+e.moduleId+'" failed'),console.error(e),console.error("Here are the modules that depend on it:"),void console.error(e.neededBy);"factory"===e.phase&&(console.error('The factory function of "'+e.moduleId+'" has thrown an exception'),console.error(e),console.error("Here are the modules that depend on it:"),console.error(e.neededBy))}),Array.isArray(e.ignoreDuplicateModules)||(e.ignoreDuplicateModules=[]),0<e.baseUrl.length&&(u.Utilities.endsWith(e.baseUrl,"/")||(e.baseUrl+="/")),"string"!=typeof e.cspNonce&&(e.cspNonce=""),"u"<typeof e.preferScriptTags&&(e.preferScriptTags=!1),e.nodeCachedData&&"object"==typeof e.nodeCachedData&&("string"!=typeof e.nodeCachedData.seed&&(e.nodeCachedData.seed="seed"),("number"!=typeof e.nodeCachedData.writeDelay||e.nodeCachedData.writeDelay<0)&&(e.nodeCachedData.writeDelay=7e3),!e.nodeCachedData.path||"string"!=typeof e.nodeCachedData.path)&&((t=r(new Error("INVALID cached data configuration, 'path' MUST be set"))).phase="configuration",e.onError(t),e.nodeCachedData=void 0),e},n.mergeConfigurationOptions=function(e,t){void 0===e&&(e=null);var r=u.Utilities.recursiveClone((t=void 0===t?null:t)||{});return u.Utilities.forEachProperty(e,function(e,t){"ignoreDuplicateModules"===e&&typeof r.ignoreDuplicateModules<"u"?r.ignoreDuplicateModules=r.ignoreDuplicateModules.concat(t):"paths"===e&&typeof r.paths<"u"?u.Utilities.forEachProperty(t,function(e,t){return r.paths[e]=t}):"config"===e&&typeof r.config<"u"?u.Utilities.forEachProperty(t,function(e,t){return r.config[e]=t}):r[e]=u.Utilities.recursiveClone(t)}),n.validateConfigurationOptions(r)};var o=n;function n(){}function t(e,t){this._env=e,this.options=o.mergeConfigurationOptions(t),this._createIgnoreDuplicateModulesMap(),this._createSortedPathsRules(),""===this.options.baseUrl&&this.options.nodeRequire&&this.options.nodeRequire.main&&this.options.nodeRequire.main.filename&&this._env.isNode&&(e=this.options.nodeRequire.main.filename,t=Math.max(e.lastIndexOf("/"),e.lastIndexOf("\\")),this.options.baseUrl=e.substring(0,t+1))}u.ConfigurationOptionsUtil=o,t.prototype._createIgnoreDuplicateModulesMap=function(){this.ignoreDuplicateModulesMap={};for(var e=0;e<this.options.ignoreDuplicateModules.length;e++)this.ignoreDuplicateModulesMap[this.options.ignoreDuplicateModules[e]]=!0},t.prototype._createSortedPathsRules=function(){var r=this;this.sortedPathsRules=[],u.Utilities.forEachProperty(this.options.paths,function(e,t){Array.isArray(t)?r.sortedPathsRules.push({from:e,to:t}):r.sortedPathsRules.push({from:e,to:[t]})}),this.sortedPathsRules.sort(function(e,t){return t.from.length-e.from.length})},t.prototype.cloneAndMerge=function(e){return new t(this._env,o.mergeConfigurationOptions(e,this.options))},t.prototype.getOptionsLiteral=function(){return this.options},t.prototype._applyPaths=function(e){for(var t,r=0,o=this.sortedPathsRules.length;r<o;r++)if(t=this.sortedPathsRules[r],u.Utilities.startsWith(e,t.from)){for(var n=[],i=0,s=t.to.length;i<s;i++)n.push(t.to[i]+e.substr(t.from.length));return n}return[e]},t.prototype._addUrlArgsToUrl=function(e){return u.Utilities.containsQueryString(e)?e+"&"+this.options.urlArgs:e+"?"+this.options.urlArgs},t.prototype._addUrlArgsIfNecessaryToUrl=function(e){return this.options.urlArgs?this._addUrlArgsToUrl(e):e},t.prototype._addUrlArgsIfNecessaryToUrls=function(e){if(this.options.urlArgs)for(var t=0,r=e.length;t<r;t++)e[t]=this._addUrlArgsToUrl(e[t]);return e},t.prototype.moduleIdToPaths=function(e){if(this._env.isNode&&(this.options.amdModulesPattern instanceof RegExp&&!this.options.amdModulesPattern.test(e)))return this.isBuild()?["empty:"]:["node|"+e];if(u.Utilities.endsWith(e,".js")||u.Utilities.isAbsolutePath(e))u.Utilities.endsWith(e,".js")||u.Utilities.containsQueryString(e)||(e+=".js"),t=[e];else for(var t,r=0,o=(t=this._applyPaths(e)).length;r<o;r++)this.isBuild()&&"empty:"===t[r]||(u.Utilities.isAbsolutePath(t[r])||(t[r]=this.options.baseUrl+t[r]),u.Utilities.endsWith(t[r],".js")||u.Utilities.containsQueryString(t[r])||(t[r]=t[r]+".js"));return this._addUrlArgsIfNecessaryToUrls(t)},t.prototype.requireToUrl=function(e){return u.Utilities.isAbsolutePath(e)||(e=this._applyPaths(e)[0],u.Utilities.isAbsolutePath(e)||(e=this.options.baseUrl+e)),this._addUrlArgsIfNecessaryToUrl(e)},t.prototype.isBuild=function(){return this.options.isBuild},t.prototype.shouldInvokeFactory=function(e){return!!(!this.options.isBuild||u.Utilities.isAnonymousModule(e)||this.options.buildForceInvokeFactory&&this.options.buildForceInvokeFactory[e])},t.prototype.isDuplicateMessageIgnoredFor=function(e){return this.ignoreDuplicateModulesMap.hasOwnProperty(e)},t.prototype.getConfigForModule=function(e){if(this.options.config)return this.options.config[e]},t.prototype.shouldCatchError=function(){return this.options.catchError},t.prototype.shouldRecordStats=function(){return this.options.recordStats},t.prototype.onError=function(e){this.options.onError(e)},u.Configuration=t}(AMDLoader=AMDLoader||{}),function(_){r.prototype.load=function(e,t,r,o){var n=this,i=(this._scriptLoader||(this._env.isWebWorker?this._scriptLoader=new u:this._env.isElectronRenderer?(i=e.getConfig().getOptionsLiteral().preferScriptTags,this._scriptLoader=i?new s:new d(this._env)):this._env.isNode?this._scriptLoader=new d(this._env):this._scriptLoader=new s),{callback:r,errorback:o});this._callbackMap.hasOwnProperty(t)?this._callbackMap[t].push(i):(this._callbackMap[t]=[i],this._scriptLoader.load(e,t,function(){return n.triggerCallback(t)},function(e){return n.triggerErrorback(t,e)}))},r.prototype.triggerCallback=function(e){var t=this._callbackMap[e];delete this._callbackMap[e];for(var r=0;r<t.length;r++)t[r].callback()},r.prototype.triggerErrorback=function(e,t){var r=this._callbackMap[e];delete this._callbackMap[e];for(var o=0;o<r.length;o++)r[o].errorback(t)};var t=r,s=(e.prototype.attachListeners=function(e,t,r){function o(){e.removeEventListener("load",n),e.removeEventListener("error",i)}var n=function(e){o(),t()},i=function(e){o(),r(e)};e.addEventListener("load",n),e.addEventListener("error",i)},e.prototype.load=function(e,t,r,o){if(/^node\|/.test(t)){var n=e.getConfig().getOptionsLiteral(),n=y(e.getRecorder(),n.nodeRequire||_.global.nodeRequire),i=t.split("|"),s=null;try{s=n(i[1])}catch(e){return void o(e)}e.enqueueDefineAnonymousModule([],function(){return s}),r()}else{n=document.createElement("script"),i=(n.setAttribute("async","async"),n.setAttribute("type","text/javascript"),this.attachListeners(n,r,o),e.getConfig().getOptionsLiteral().trustedTypesPolicy),r=(i&&(t=i.createScriptURL(t)),n.setAttribute("src",t),e.getConfig().getOptionsLiteral().cspNonce);r&&n.setAttribute("nonce",r),document.getElementsByTagName("head")[0].appendChild(n)}},e);function e(){}function r(e){this._env=e,this._scriptLoader=null,this._callbackMap={}}o.prototype._canUseEval=function(e){return null===this._cachedCanUseEval&&(this._cachedCanUseEval=function(e){e=e.getConfig().getOptionsLiteral().trustedTypesPolicy;try{return(e?self.eval(e.createScript("","true")):new Function("true")).call(self),!0}catch{return!1}}(e)),this._cachedCanUseEval},o.prototype.load=function(e,t,r,o){if(/^node\|/.test(t)){var n=e.getConfig().getOptionsLiteral(),n=y(e.getRecorder(),n.nodeRequire||_.global.nodeRequire),i=t.split("|"),s=null;try{s=n(i[1])}catch(e){return void o(e)}e.enqueueDefineAnonymousModule([],function(){return s}),r()}else{var u=e.getConfig().getOptionsLiteral().trustedTypesPolicy;if(!(/^((http:)|(https:)|(file:))/.test(t)&&t.substring(0,self.origin.length)!==self.origin)&&this._canUseEval(e))fetch(t).then(function(e){if(200!==e.status)throw new Error(e.statusText);return e.text()}).then(function(e){e=e+`
//# sourceURL=`+t,(u?self.eval(u.createScript("",e)):new Function(e)).call(self),r()}).then(void 0,o);else try{u&&(t=u.createScriptURL(t)),importScripts(t),r()}catch(e){o(e)}}};var u=o,d=(g.prototype._init=function(e){this._didInitialize||(this._didInitialize=!0,this._fs=e("fs"),this._vm=e("vm"),this._path=e("path"),this._crypto=e("crypto"))},g.prototype._initNodeRequire=function(e,a){var l,c,h=a.getConfig().getOptionsLiteral().nodeCachedData;function p(r){function e(e){return r.require(e)}var o=r.constructor;return(e.resolve=function(e,t){return o._resolveFilename(e,r,!1,t)}).paths=function(e){return o._resolveLookupPaths(e,r)},e.main=process.mainModule,e.extensions=o._extensions,e.cache=o._cache,e}h&&!this._didPatchNodeRequire&&(this._didPatchNodeRequire=!0,l=this,(c=e("module")).prototype._compile=function(e,t){var e=c.wrap(e.replace(/^#!.*/,"")),r=a.getRecorder(),o=l._getCachedDataPath(h,t),n={filename:t};try{var i=l._fs.readFileSync(o),s=i.slice(0,16);n.cachedData=i.slice(16),r.record(60,o)}catch{r.record(61,o)}var i=new l._vm.Script(e,n),r=i.runInThisContext(n),u=l._path.dirname(t),d=p(this),d=[this.exports,d,this,t,u,process,_commonjsGlobal,Buffer],t=r.apply(this.exports,d);return l._handleCachedData(i,e,o,!n.cachedData,a),l._verifyCachedData(i,e,o,s,a),t})},g.prototype.load=function(n,e,i,s){var u=this,t=n.getConfig().getOptionsLiteral(),r=y(n.getRecorder(),t.nodeRequire||_.global.nodeRequire),d=t.nodeInstrumenter||function(e){return e},o=(this._init(r),this._initNodeRequire(r,n),n.getRecorder());if(/^node\|/.test(e)){var a=e.split("|"),l=null;try{l=r(a[1])}catch(e){return void s(e)}n.enqueueDefineAnonymousModule([],function(){return l}),i()}else{e=_.Utilities.fileUriToFilePath(this._env.isWindows,e);var c=this._path.normalize(e),h=this._getElectronRendererScriptPathOrUri(c),p=Boolean(t.nodeCachedData),f=p?this._getCachedDataPath(t.nodeCachedData,e):void 0;this._readSourceAndCachedData(c,f,o,function(e,t,r,o){e?s(e):(e=t.charCodeAt(0)===g._BOM?g._PREFIX+t.substring(1)+g._SUFFIX:g._PREFIX+t+g._SUFFIX,e=d(e,c),t=u._createAndEvalScript(n,e,{filename:h,cachedData:r},i,s),u._handleCachedData(t,e,f,p&&!r,n),u._verifyCachedData(t,e,f,o,n))})}},g.prototype._createAndEvalScript=function(e,t,r,o,n){function i(){return a=!0,d.apply(null,arguments)}var s=e.getRecorder(),t=(s.record(31,r.filename),new this._vm.Script(t,r)),u=t.runInThisContext(r),d=e.getGlobalAMDDefineFunc(),a=!1;return i.amd=d.amd,u.call(_.global,e.getGlobalAMDRequireFunc(),i,r.filename,this._path.dirname(r.filename)),s.record(32,r.filename),a?o():n(new Error("Didn't receive define call in "+r.filename+"!")),t},g.prototype._getElectronRendererScriptPathOrUri=function(e){if(!this._env.isElectronRenderer)return e;var t=e.match(/^([a-z])\:(.*)/i);return t?"file:///"+(t[1].toUpperCase()+":"+t[2]).replace(/\\/g,"/"):"file://"+e},g.prototype._getCachedDataPath=function(e,t){var r=this._crypto.createHash("md5").update(t,"utf8").update(e.seed,"utf8").update(process.arch,"").digest("hex"),t=this._path.basename(t).replace(/\.js$/,"");return this._path.join(e.path,t+"-"+r+".code")},g.prototype._handleCachedData=function(t,r,o,e,n){var i=this;t.cachedDataRejected?this._fs.unlink(o,function(e){n.getRecorder().record(62,o),i._createAndWriteCachedData(t,r,o,n),e&&n.getConfig().onError(e)}):e&&this._createAndWriteCachedData(t,r,o,n)},g.prototype._createAndWriteCachedData=function(t,r,o,n){var i=this,e=Math.ceil(n.getConfig().getOptionsLiteral().nodeCachedData.writeDelay*(1+Math.random())),s=-1,u=0,d=void 0,a=function(){setTimeout(function(){d=d||i._crypto.createHash("md5").update(r,"utf8").digest();var e=t.createCachedData();0===e.length||e.length===s||5<=u||(e.length<s?a():(s=e.length,i._fs.writeFile(o,Buffer.concat([d,e]),function(e){e&&n.getConfig().onError(e),n.getRecorder().record(63,o),a()})))},e*Math.pow(4,u++))};a()},g.prototype._readSourceAndCachedData=function(e,r,o,t){var n,i,s,u,d;r?(s=i=n=void 0,u=2,d=function(e){e?t(e):0==--u&&t(void 0,n,i,s)},this._fs.readFile(e,{encoding:"utf8"},function(e,t){n=t,d(e)}),this._fs.readFile(r,function(e,t){!e&&t&&0<t.length?(s=t.slice(0,16),i=t.slice(16),o.record(60,r)):o.record(61,r),d()})):this._fs.readFile(e,{encoding:"utf8"},t)},g.prototype._verifyCachedData=function(e,t,r,o,n){var i=this;o&&!e.cachedDataRejected&&setTimeout(function(){var e=i._crypto.createHash("md5").update(t,"utf8").digest();o.equals(e)||(n.getConfig().onError(new Error("FAILED TO VERIFY CACHED DATA, deleting stale '"+r+"' now, but a RESTART IS REQUIRED")),i._fs.unlink(r,function(e){e&&n.getConfig().onError(e)}))},Math.ceil(5e3*(1+Math.random())))},g._BOM=65279,g._PREFIX="(function (require, define, __filename, __dirname) { ",g._SUFFIX=`
});`,g);function g(e){this._env=e,this._didInitialize=!1,this._didPatchNodeRequire=!1}function o(){this._cachedCanUseEval=null}function y(t,r){if(r.__$__isRecorded)return r;function e(e){t.record(33,e);try{return r(e)}finally{t.record(34,e)}}return e.__$__isRecorded=!0,e}_.ensureRecordedNodeRequire=y,_.createScriptLoader=function(e){return new t(e)}}(AMDLoader=AMDLoader||{}),function(i){t._normalizeModuleId=function(e){for(var t=e,r=/\/\.\//;r.test(t);)t=t.replace(r,"/");for(t=t.replace(/^\.\//g,""),r=/\/(([^\/])|([^\/][^\/\.])|([^\/\.][^\/])|([^\/][^\/][^\/]+))\/\.\.\//;r.test(t);)t=t.replace(r,"/");return t=t.replace(/^(([^\/])|([^\/][^\/\.])|([^\/\.][^\/])|([^\/][^\/][^\/]+))\/\.\.\//,"")},t.prototype.resolveModule=function(e){return i.Utilities.isAbsolutePath(e)||(i.Utilities.startsWith(e,"./")||i.Utilities.startsWith(e,"../"))&&(e=t._normalizeModuleId(this.fromModulePath+e)),e},t.ROOT=new t("");var d=t;function t(e){var t=e.lastIndexOf("/");this.fromModulePath=-1!==t?e.substr(0,t+1):""}i.ModuleIdResolver=d;s._safeInvokeFunction=function(e,t){try{return{returnedValue:e.apply(i.global,t),producedError:null}}catch(e){return{returnedValue:null,producedError:e}}},s._invokeFactory=function(e,t,r,o){return e.shouldInvokeFactory(t)?e.shouldCatchError()?this._safeInvokeFunction(r,o):{returnedValue:r.apply(i.global,o),producedError:null}:{returnedValue:null,producedError:null}},s.prototype.complete=function(e,t,r,o){this._isComplete=!0;var n=null;this._callback&&("function"==typeof this._callback?(e.record(21,this.strId),n=(r=s._invokeFactory(t,this.strId,this._callback,r)).producedError,e.record(22,this.strId),!n&&typeof r.returnedValue<"u"&&(!this.exportsPassedIn||i.Utilities.isEmpty(this.exports))&&(this.exports=r.returnedValue)):this.exports=this._callback),n&&((e=i.ensureError(n)).phase="factory",e.moduleId=this.strId,e.neededBy=o(this.id),this.error=e,t.onError(e)),this.dependencies=null,this._callback=null,this._errorback=null,this.moduleIdResolver=null},s.prototype.onDependencyError=function(e){return this._isComplete=!0,this.error=e,!!this._errorback&&(this._errorback(e),!0)},s.prototype.isComplete=function(){return this._isComplete};var h=s;function s(e,t,r,o,n,i){this.id=e,this.strId=t,this.dependencies=r,this._callback=o,this._errorback=n,this.moduleIdResolver=i,this.exports={},this.error=null,this.exportsPassedIn=!1,this.unresolvedDependenciesCount=this.dependencies.length,this._isComplete=!1}i.Module=h;r.prototype.getMaxModuleId=function(){return this._nextId},r.prototype.getModuleId=function(e){var t=this._strModuleIdToIntModuleId.get(e);return"u"<typeof t&&(t=this._nextId++,this._strModuleIdToIntModuleId.set(e,t),this._intModuleIdToStrModuleId[t]=e),t},r.prototype.getStrModuleId=function(e){return this._intModuleIdToStrModuleId[e]};var u=r,c=(e.EXPORTS=new e(0),e.MODULE=new e(1),e.REQUIRE=new e(2),e);function e(e){this.id=e}function r(){this._nextId=0,this._strModuleIdToIntModuleId=new Map,this._intModuleIdToStrModuleId=[],this.getModuleId("exports"),this.getModuleId("module"),this.getModuleId("require")}i.RegularDependency=c;var a=function(e,t,r){this.id=e,this.pluginId=t,this.pluginParam=r},o=(i.PluginDependency=a,l.prototype.reset=function(){return new l(this._env,this._scriptLoader,this._defineFunc,this._requireFunc,this._loaderAvailableTimestamp)},l.prototype.getGlobalAMDDefineFunc=function(){return this._defineFunc},l.prototype.getGlobalAMDRequireFunc=function(){return this._requireFunc},l._findRelevantLocationInStack=function(e,t){for(var r=function(e){return e.replace(/\\/g,"/")},o=r(e),n=t.split(/\n/),i=0;i<n.length;i++){var s=n[i].match(/(.*):(\d+):(\d+)\)?$/);if(s){var u=s[1],d=s[2],s=s[3],a=Math.max(u.lastIndexOf(" ")+1,u.lastIndexOf("(")+1);if((u=r(u=u.substr(a)))===o)return 1===(a={line:parseInt(d,10),col:parseInt(s,10)}).line&&(a.col-=53),a}}throw new Error("Could not correlate define call site for needle "+e)},l.prototype.getBuildInfo=function(){if(!this._config.isBuild())return null;for(var e=[],t=0,r=0,o=this._modules2.length;r<o;r++){var n,i,s,u=this._modules2[r];u&&(n=this._buildInfoPath[u.id]||null,i=this._buildInfoDefineStack[u.id]||null,s=this._buildInfoDependencies[u.id],e[t++]={id:u.strId,path:n,defineLocation:n&&i?l._findRelevantLocationInStack(n,i):null,dependencies:s,shim:null,exports:u.exports})}return e},l.prototype.getRecorder=function(){return this._recorder||(this._config.shouldRecordStats()?this._recorder=new i.LoaderEventRecorder(this._loaderAvailableTimestamp):this._recorder=i.NullLoaderEventRecorder.INSTANCE),this._recorder},l.prototype.getLoaderEvents=function(){return this.getRecorder().getEvents()},l.prototype.enqueueDefineAnonymousModule=function(e,t){if(null!==this._currentAnonymousDefineCall)throw new Error("Can only have one anonymous define call per script file");var r=null;this._config.isBuild()&&(r=new Error("StackLocation").stack||null),this._currentAnonymousDefineCall={stack:r,dependencies:e,callback:t}},l.prototype.defineModule=function(e,t,r,o,n,i){var s=this,u=(void 0===i&&(i=new d(e)),this._moduleIdProvider.getModuleId(e));this._modules2[u]?this._config.isDuplicateMessageIgnoredFor(e)||console.warn("Duplicate definition of module '"+e+"'"):(e=new h(u,e,this._normalizeDependencies(t,i),r,o,i),this._modules2[u]=e,this._config.isBuild()&&(this._buildInfoDefineStack[u]=n,this._buildInfoDependencies[u]=(e.dependencies||[]).map(function(e){return s._moduleIdProvider.getStrModuleId(e.id)})),this._resolve(e))},l.prototype._normalizeDependency=function(e,t){if("exports"===e)return c.EXPORTS;if("module"===e)return c.MODULE;if("require"===e)return c.REQUIRE;var r,o,n=e.indexOf("!");return 0<=n?(o=t.resolveModule(e.substr(0,n)),n=t.resolveModule(e.substr(n+1)),r=this._moduleIdProvider.getModuleId(o+"!"+n),o=this._moduleIdProvider.getModuleId(o),new a(r,o,n)):new c(this._moduleIdProvider.getModuleId(t.resolveModule(e)))},l.prototype._normalizeDependencies=function(e,t){for(var r=[],o=0,n=0,i=e.length;n<i;n++)r[o++]=this._normalizeDependency(e[n],t);return r},l.prototype._relativeRequire=function(e,t,r,o){if("string"==typeof t)return this.synchronousRequire(t,e);this.defineModule(i.Utilities.generateAnonymousModule(),t,r,o,null,e)},l.prototype.synchronousRequire=function(e,t){void 0===t&&(t=new d(e));t=this._normalizeDependency(e,t),t=this._modules2[t.id];if(!t)throw new Error("Check dependency list! Synchronous require cannot resolve module '"+e+"'. This is the first mention of this module!");if(!t.isComplete())throw new Error("Check dependency list! Synchronous require cannot resolve module '"+e+"'. This module has not been resolved completely yet.");if(t.error)throw t.error;return t.exports},l.prototype.configure=function(e,t){var r=this._config.shouldRecordStats();this._config=t?new i.Configuration(this._env,e):this._config.cloneAndMerge(e),this._config.shouldRecordStats()&&!r&&(this._recorder=null)},l.prototype.getConfig=function(){return this._config},l.prototype._onLoad=function(e){var t;null!==this._currentAnonymousDefineCall&&(t=this._currentAnonymousDefineCall,this._currentAnonymousDefineCall=null,this.defineModule(this._moduleIdProvider.getStrModuleId(e),t.dependencies,t.callback,null,t.stack))},l.prototype._createLoadError=function(e,t){var r=this,o=this._moduleIdProvider.getStrModuleId(e),e=(this._inverseDependencies2[e]||[]).map(function(e){return r._moduleIdProvider.getStrModuleId(e)}),t=i.ensureError(t);return t.phase="loading",t.moduleId=o,t.neededBy=e,t},l.prototype._onLoadError=function(e,t){var r=this._createLoadError(e,t);this._modules2[e]||(this._modules2[e]=new h(e,this._moduleIdProvider.getStrModuleId(e),[],function(){},null,null));for(var o=[],n=0,i=this._moduleIdProvider.getMaxModuleId();n<i;n++)o[n]=!1;var s=!1,u=[];for(u.push(e),o[e]=!0;0<u.length;){var d=u.shift(),a=this._modules2[d],l=(a&&(s=a.onDependencyError(r)||s),this._inverseDependencies2[d]);if(l)for(n=0,i=l.length;n<i;n++){var c=l[n];o[c]||(u.push(c),o[c]=!0)}}s||this._config.onError(r)},l.prototype._hasDependencyPath=function(e,t){var r=this._modules2[e];if(!r)return!1;for(var o=[],n=0,i=this._moduleIdProvider.getMaxModuleId();n<i;n++)o[n]=!1;var s=[];for(s.push(r),o[e]=!0;0<s.length;){var u=s.shift().dependencies;if(u)for(n=0,i=u.length;n<i;n++){var d=u[n];if(d.id===t)return!0;var a=this._modules2[d.id];a&&!o[d.id]&&(o[d.id]=!0,s.push(a))}}return!1},l.prototype._findCyclePath=function(e,t,r){if(e===t||50===r)return[e];var o=this._modules2[e];if(!o)return null;var n=o.dependencies;if(n)for(var i=0,s=n.length;i<s;i++){var u=this._findCyclePath(n[i].id,t,r+1);if(null!==u)return u.push(e),u}return null},l.prototype._createRequire=function(o){function e(e,t,r){return n._relativeRequire(o,e,t,r)}var n=this;return e.toUrl=function(e){return n._config.requireToUrl(o.resolveModule(e))},e.getStats=function(){return n.getLoaderEvents()},e.hasDependencyCycle=function(){return n._hasDependencyCycle},e.config=function(e,t){n.configure(e,t=void 0===t?!1:t)},e.__$__nodeRequire=i.global.nodeRequire,e},l.prototype._loadModule=function(o){var e,n,i,s,u=this;this._modules2[o]||this._knownModules2[o]||(this._knownModules2[o]=!0,e=this._moduleIdProvider.getStrModuleId(o),n=this._config.moduleIdToPaths(e),this._env.isNode&&(-1===e.indexOf("/")||/^@[^\/]+\/[^\/]+$/.test(e))&&n.push("node|"+e),i=-1,(s=function(e){if(++i>=n.length)u._onLoadError(o,e);else{var t=n[i],r=u.getRecorder();if(u._config.isBuild()&&"empty:"===t)return u._buildInfoPath[o]=t,u.defineModule(u._moduleIdProvider.getStrModuleId(o),[],null,null,null),void u._onLoad(o);r.record(10,t),u._scriptLoader.load(u,t,function(){u._config.isBuild()&&(u._buildInfoPath[o]=t),r.record(11,t),u._onLoad(o)},function(e){r.record(12,t),s(e)})}})(null))},l.prototype._loadPluginDependency=function(e,t){var r,o=this;this._modules2[t.id]||this._knownModules2[t.id]||(this._knownModules2[t.id]=!0,(r=function(e){o.defineModule(o._moduleIdProvider.getStrModuleId(t.id),[],e,null,null)}).error=function(e){o._config.onError(o._createLoadError(t.id,e))},e.load(t.pluginParam,this._createRequire(d.ROOT),r,this._config.getOptionsLiteral()))},l.prototype._resolve=function(e){var t=this,r=e.dependencies;if(r)for(var o=0,n=r.length;o<n;o++){var i=r[o];if(i===c.EXPORTS)e.exportsPassedIn=!0,e.unresolvedDependenciesCount--;else if(i===c.MODULE)e.unresolvedDependenciesCount--;else if(i===c.REQUIRE)e.unresolvedDependenciesCount--;else{var s=this._modules2[i.id];if(s&&s.isComplete()){if(s.error)return void e.onDependencyError(s.error);e.unresolvedDependenciesCount--}else this._hasDependencyPath(i.id,e.id)?(this._hasDependencyCycle=!0,console.warn("There is a dependency cycle between '"+this._moduleIdProvider.getStrModuleId(i.id)+"' and '"+this._moduleIdProvider.getStrModuleId(e.id)+"'. The cyclic path follows:"),(s=this._findCyclePath(i.id,e.id,0)||[]).reverse(),s.push(i.id),console.warn(s.map(function(e){return t._moduleIdProvider.getStrModuleId(e)}).join(` => 
`)),e.unresolvedDependenciesCount--):(this._inverseDependencies2[i.id]=this._inverseDependencies2[i.id]||[],this._inverseDependencies2[i.id].push(e.id),i instanceof a?(s=this._modules2[i.pluginId])&&s.isComplete()?this._loadPluginDependency(s.exports,i):((s=this._inversePluginDependencies2.get(i.pluginId))||this._inversePluginDependencies2.set(i.pluginId,s=[]),s.push(i),this._loadModule(i.pluginId)):this._loadModule(i.id))}}0===e.unresolvedDependenciesCount&&this._onModuleComplete(e)},l.prototype._onModuleComplete=function(e){var t=this,r=this.getRecorder();if(!e.isComplete()){var o=e.dependencies,n=[];if(o)for(var i=0,s=o.length;i<s;i++){var u=o[i];u===c.EXPORTS?n[i]=e.exports:u===c.MODULE?n[i]={id:e.strId,config:function(){return t._config.getConfigForModule(e.strId)}}:u===c.REQUIRE?n[i]=this._createRequire(e.moduleIdResolver):(u=this._modules2[u.id],n[i]=u?u.exports:null)}e.complete(r,this._config,n,function(e){return(t._inverseDependencies2[e]||[]).map(function(e){return t._moduleIdProvider.getStrModuleId(e)})});var d=this._inverseDependencies2[e.id];if(this._inverseDependencies2[e.id]=null,d)for(i=0,s=d.length;i<s;i++){var a=d[i],a=this._modules2[a];a.unresolvedDependenciesCount--,0===a.unresolvedDependenciesCount&&this._onModuleComplete(a)}var l=this._inversePluginDependencies2.get(e.id);if(l){this._inversePluginDependencies2.delete(e.id);for(i=0,s=l.length;i<s;i++)this._loadPluginDependency(e.exports,l[i])}}},l);function l(e,t,r,o,n){void 0===n&&(n=0),this._env=e,this._scriptLoader=t,this._loaderAvailableTimestamp=n,this._defineFunc=r,this._requireFunc=o,this._moduleIdProvider=new u,this._config=new i.Configuration(this._env),this._hasDependencyCycle=!1,this._modules2=[],this._knownModules2=[],this._inverseDependencies2=[],this._inversePluginDependencies2=new Map,this._currentAnonymousDefineCall=null,this._recorder=null,this._buildInfoPath=[],this._buildInfoDefineStack=[],this._buildInfoDependencies=[]}i.ModuleManager=o}(AMDLoader=AMDLoader||{}),function(t){function r(e,t,r){"string"!=typeof e&&(r=t,t=e,e=null),"object"==typeof t&&Array.isArray(t)||(r=t,t=null),t=t||["require","exports","module"],e?i.defineModule(e,t,r,null,null):i.enqueueDefineAnonymousModule(t,r)}function e(e,t){i.configure(e,t=void 0===t?!1:t)}function o(){if(1===arguments.length){if(arguments[0]instanceof Object&&!Array.isArray(arguments[0]))return void e(arguments[0]);if("string"==typeof arguments[0])return i.synchronousRequire(arguments[0])}if(2!==arguments.length&&3!==arguments.length||!Array.isArray(arguments[0]))throw new Error("Unrecognized require call");i.defineModule(t.Utilities.generateAnonymousModule(),arguments[0],arguments[1],arguments[2],null)}var n=new t.Environment,i=null;r.amd={jQuery:!0};function s(){var e;(typeof t.global.require<"u"||typeof require<"u")&&"function"==typeof(e=t.global.require||require)&&"function"==typeof e.resolve&&(e=t.ensureRecordedNodeRequire(i.getRecorder(),e),t.global.nodeRequire=e,o.nodeRequire=e,o.__$__nodeRequire=e),!n.isNode||n.isElectronRenderer||n.isElectronNodeIntegrationWebWorker?(n.isElectronRenderer||(t.global.define=r),t.global.require=o):module.exports=o}o.config=e,o.getConfig=function(){return i.getConfig().getOptionsLiteral()},o.reset=function(){i=i.reset()},o.getBuildInfo=function(){return i.getBuildInfo()},o.getStats=function(){return i.getLoaderEvents()},o.define=r,t.init=s,"function"==typeof t.global.define&&t.global.define.amd||(i=new t.ModuleManager(n,t.createScriptLoader(n),r,o,t.Utilities.getHighPerformanceTimestamp()),typeof t.global.require<"u"&&"function"!=typeof t.global.require&&o.config(t.global.require),(define=function(){return r.apply(null,arguments)}).amd=r.amd,"u"<typeof doNotInitLoader&&s())}(AMDLoader=AMDLoader||{});