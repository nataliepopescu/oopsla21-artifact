// Loaded from https://dev.jspm.io/npm:@jspm/core@1.1.1/nodelibs/chunk-dac557ba.js


import { h as h$1 } from "./chunk-0c2d1322.js";

var t = "function" == typeof Symbol && "symbol" == typeof Symbol.toStringTag,
    e = Object.prototype.toString,
    o = function (o) {
  return !(t && o && "object" == typeof o && Symbol.toStringTag in o) && "[object Arguments]" === e.call(o);
},
    n = function (t) {
  return !!o(t) || null !== t && "object" == typeof t && "number" == typeof t.length && t.length >= 0 && "[object Array]" !== e.call(t) && "[object Function]" === e.call(t.callee);
},
    r = function () {
  return o(arguments);
}();

o.isLegacyArguments = n;
var l = r ? o : n;

var t$1 = Object.prototype.toString,
    o$1 = Function.prototype.toString,
    n$1 = /^\s*(?:function)?\*/,
    e$1 = "function" == typeof Symbol && "symbol" == typeof Symbol.toStringTag,
    r$1 = Object.getPrototypeOf,
    c = function () {
  if (!e$1) return !1;

  try {
    return Function("return function*() {}")();
  } catch (t) {}
}(),
    u = c ? r$1(c) : {},
    i = function (c) {
  return "function" == typeof c && (!!n$1.test(o$1.call(c)) || (e$1 ? r$1(c) === u : "[object GeneratorFunction]" === t$1.call(c)));
};

var t$2 = "function" == typeof Object.create ? function (t, e) {
  e && (t.super_ = e, t.prototype = Object.create(e.prototype, {
    constructor: {
      value: t,
      enumerable: !1,
      writable: !0,
      configurable: !0
    }
  }));
} : function (t, e) {
  if (e) {
    t.super_ = e;

    var o = function () {};

    o.prototype = e.prototype, t.prototype = new o(), t.prototype.constructor = t;
  }
};

var i$1 = function (e) {
  return e && "object" == typeof e && "function" == typeof e.copy && "function" == typeof e.fill && "function" == typeof e.readUInt8;
},
    o$2 = {},
    u$1 = i$1,
    f = l,
    a = i;

function c$1(e) {
  return e.call.bind(e);
}

var s = "undefined" != typeof BigInt,
    p = "undefined" != typeof Symbol,
    y = p && void 0 !== Symbol.toStringTag,
    l$1 = "undefined" != typeof Uint8Array,
    d = "undefined" != typeof ArrayBuffer;
if (l$1 && y) var g = Object.getPrototypeOf(Uint8Array.prototype),
    b = c$1(Object.getOwnPropertyDescriptor(g, Symbol.toStringTag).get);
var m = c$1(Object.prototype.toString),
    h = c$1(Number.prototype.valueOf),
    j = c$1(String.prototype.valueOf),
    A = c$1(Boolean.prototype.valueOf);
if (s) var w = c$1(BigInt.prototype.valueOf);
if (p) var v = c$1(Symbol.prototype.valueOf);

function O(e, t) {
  if ("object" != typeof e) return !1;

  try {
    return t(e), !0;
  } catch (e) {
    return !1;
  }
}

function S(e) {
  return l$1 && y ? void 0 !== b(e) : B(e) || k(e) || E(e) || D(e) || U(e) || P(e) || x(e) || I(e) || M(e) || z(e) || F(e);
}

function B(e) {
  return l$1 && y ? "Uint8Array" === b(e) : "[object Uint8Array]" === m(e) || u$1(e) && void 0 !== e.buffer;
}

function k(e) {
  return l$1 && y ? "Uint8ClampedArray" === b(e) : "[object Uint8ClampedArray]" === m(e);
}

function E(e) {
  return l$1 && y ? "Uint16Array" === b(e) : "[object Uint16Array]" === m(e);
}

function D(e) {
  return l$1 && y ? "Uint32Array" === b(e) : "[object Uint32Array]" === m(e);
}

function U(e) {
  return l$1 && y ? "Int8Array" === b(e) : "[object Int8Array]" === m(e);
}

function P(e) {
  return l$1 && y ? "Int16Array" === b(e) : "[object Int16Array]" === m(e);
}

function x(e) {
  return l$1 && y ? "Int32Array" === b(e) : "[object Int32Array]" === m(e);
}

function I(e) {
  return l$1 && y ? "Float32Array" === b(e) : "[object Float32Array]" === m(e);
}

function M(e) {
  return l$1 && y ? "Float64Array" === b(e) : "[object Float64Array]" === m(e);
}

function z(e) {
  return l$1 && y ? "BigInt64Array" === b(e) : "[object BigInt64Array]" === m(e);
}

function F(e) {
  return l$1 && y ? "BigUint64Array" === b(e) : "[object BigUint64Array]" === m(e);
}

function T(e) {
  return "[object Map]" === m(e);
}

function N(e) {
  return "[object Set]" === m(e);
}

function W(e) {
  return "[object WeakMap]" === m(e);
}

function $(e) {
  return "[object WeakSet]" === m(e);
}

function C(e) {
  return "[object ArrayBuffer]" === m(e);
}

function V(e) {
  return "undefined" != typeof ArrayBuffer && (C.working ? C(e) : e instanceof ArrayBuffer);
}

function G(e) {
  return "[object DataView]" === m(e);
}

function R(e) {
  return "undefined" != typeof DataView && (G.working ? G(e) : e instanceof DataView);
}

function J(e) {
  return "[object SharedArrayBuffer]" === m(e);
}

function _(e) {
  return "undefined" != typeof SharedArrayBuffer && (J.working ? J(e) : e instanceof SharedArrayBuffer);
}

function H(e) {
  return O(e, h);
}

function Z(e) {
  return O(e, j);
}

function q(e) {
  return O(e, A);
}

function K(e) {
  return s && O(e, w);
}

function L(e) {
  return p && O(e, v);
}

o$2.isArgumentsObject = f, o$2.isGeneratorFunction = a, o$2.isPromise = function (e) {
  return "undefined" != typeof Promise && e instanceof Promise || null !== e && "object" == typeof e && "function" == typeof e.then && "function" == typeof e.catch;
}, o$2.isArrayBufferView = function (e) {
  return d && ArrayBuffer.isView ? ArrayBuffer.isView(e) : S(e) || R(e);
}, o$2.isTypedArray = S, o$2.isUint8Array = B, o$2.isUint8ClampedArray = k, o$2.isUint16Array = E, o$2.isUint32Array = D, o$2.isInt8Array = U, o$2.isInt16Array = P, o$2.isInt32Array = x, o$2.isFloat32Array = I, o$2.isFloat64Array = M, o$2.isBigInt64Array = z, o$2.isBigUint64Array = F, T.working = "undefined" != typeof Map && T(new Map()), o$2.isMap = function (e) {
  return "undefined" != typeof Map && (T.working ? T(e) : e instanceof Map);
}, N.working = "undefined" != typeof Set && N(new Set()), o$2.isSet = function (e) {
  return "undefined" != typeof Set && (N.working ? N(e) : e instanceof Set);
}, W.working = "undefined" != typeof WeakMap && W(new WeakMap()), o$2.isWeakMap = function (e) {
  return "undefined" != typeof WeakMap && (W.working ? W(e) : e instanceof WeakMap);
}, $.working = "undefined" != typeof WeakSet && $(new WeakSet()), o$2.isWeakSet = function (e) {
  return $(e);
}, C.working = "undefined" != typeof ArrayBuffer && C(new ArrayBuffer()), o$2.isArrayBuffer = V, G.working = "undefined" != typeof ArrayBuffer && "undefined" != typeof DataView && G(new DataView(new ArrayBuffer(1), 0, 1)), o$2.isDataView = R, J.working = "undefined" != typeof SharedArrayBuffer && J(new SharedArrayBuffer()), o$2.isSharedArrayBuffer = _, o$2.isAsyncFunction = function (e) {
  return "[object AsyncFunction]" === m(e);
}, o$2.isMapIterator = function (e) {
  return "[object Map Iterator]" === m(e);
}, o$2.isSetIterator = function (e) {
  return "[object Set Iterator]" === m(e);
}, o$2.isGeneratorObject = function (e) {
  return "[object Generator]" === m(e);
}, o$2.isWebAssemblyCompiledModule = function (e) {
  return "[object WebAssembly.Module]" === m(e);
}, o$2.isNumberObject = H, o$2.isStringObject = Z, o$2.isBooleanObject = q, o$2.isBigIntObject = K, o$2.isSymbolObject = L, o$2.isBoxedPrimitive = function (e) {
  return H(e) || Z(e) || q(e) || K(e) || L(e);
}, o$2.isAnyArrayBuffer = function (e) {
  return l$1 && (V(e) || _(e));
}, ["isProxy", "isExternal", "isModuleNamespaceObject"].forEach(function (e) {
  Object.defineProperty(o$2, e, {
    enumerable: !1,
    value: function () {
      throw new Error(e + " is not supported in userland");
    }
  });
});

var Q = "undefined" != typeof globalThis ? globalThis : "undefined" != typeof self ? self : global,
    X = {},
    Y = h$1,
    ee = Object.getOwnPropertyDescriptors || function (e) {
  for (var t = Object.keys(e), r = {}, n = 0; n < t.length; n++) r[t[n]] = Object.getOwnPropertyDescriptor(e, t[n]);

  return r;
},
    te = /%[sdj%]/g;

X.format = function (e) {
  if (!ge(e)) {
    for (var t = [], r = 0; r < arguments.length; r++) t.push(oe(arguments[r]));

    return t.join(" ");
  }

  r = 1;

  for (var n = arguments, i = n.length, o = String(e).replace(te, function (e) {
    if ("%%" === e) return "%";
    if (r >= i) return e;

    switch (e) {
      case "%s":
        return String(n[r++]);

      case "%d":
        return Number(n[r++]);

      case "%j":
        try {
          return JSON.stringify(n[r++]);
        } catch (e) {
          return "[Circular]";
        }

      default:
        return e;
    }
  }), u = n[r]; r < i; u = n[++r]) le(u) || !he(u) ? o += " " + u : o += " " + oe(u);

  return o;
}, X.deprecate = function (e, t) {
  if (void 0 !== Y && !0 === Y.noDeprecation) return e;
  if (void 0 === Y) return function () {
    return X.deprecate(e, t).apply(this || Q, arguments);
  };
  var r = !1;
  return function () {
    if (!r) {
      if (Y.throwDeprecation) throw new Error(t);
      Y.traceDeprecation ? console.trace(t) : console.error(t), r = !0;
    }

    return e.apply(this || Q, arguments);
  };
};
var re = {},
    ne = /^$/;

if (Y.env.NODE_DEBUG) {
  var ie = Y.env.NODE_DEBUG;
  ie = ie.replace(/[|\\{}()[\]^$+?.]/g, "\\$&").replace(/\*/g, ".*").replace(/,/g, "$|^").toUpperCase(), ne = new RegExp("^" + ie + "$", "i");
}

function oe(e, t) {
  var r = {
    seen: [],
    stylize: fe
  };
  return arguments.length >= 3 && (r.depth = arguments[2]), arguments.length >= 4 && (r.colors = arguments[3]), ye(t) ? r.showHidden = t : t && X._extend(r, t), be(r.showHidden) && (r.showHidden = !1), be(r.depth) && (r.depth = 2), be(r.colors) && (r.colors = !1), be(r.customInspect) && (r.customInspect = !0), r.colors && (r.stylize = ue), ae(r, e, r.depth);
}

function ue(e, t) {
  var r = oe.styles[t];
  return r ? "[" + oe.colors[r][0] + "m" + e + "[" + oe.colors[r][1] + "m" : e;
}

function fe(e, t) {
  return e;
}

function ae(e, t, r) {
  if (e.customInspect && t && we(t.inspect) && t.inspect !== X.inspect && (!t.constructor || t.constructor.prototype !== t)) {
    var n = t.inspect(r, e);
    return ge(n) || (n = ae(e, n, r)), n;
  }

  var i = function (e, t) {
    if (be(t)) return e.stylize("undefined", "undefined");

    if (ge(t)) {
      var r = "'" + JSON.stringify(t).replace(/^"|"$/g, "").replace(/'/g, "\\'").replace(/\\"/g, '"') + "'";
      return e.stylize(r, "string");
    }

    if (de(t)) return e.stylize("" + t, "number");
    if (ye(t)) return e.stylize("" + t, "boolean");
    if (le(t)) return e.stylize("null", "null");
  }(e, t);

  if (i) return i;

  var o = Object.keys(t),
      u = function (e) {
    var t = {};
    return e.forEach(function (e, r) {
      t[e] = !0;
    }), t;
  }(o);

  if (e.showHidden && (o = Object.getOwnPropertyNames(t)), Ae(t) && (o.indexOf("message") >= 0 || o.indexOf("description") >= 0)) return ce(t);

  if (0 === o.length) {
    if (we(t)) {
      var f = t.name ? ": " + t.name : "";
      return e.stylize("[Function" + f + "]", "special");
    }

    if (me(t)) return e.stylize(RegExp.prototype.toString.call(t), "regexp");
    if (je(t)) return e.stylize(Date.prototype.toString.call(t), "date");
    if (Ae(t)) return ce(t);
  }

  var a,
      c = "",
      s = !1,
      p = ["{", "}"];
  (pe(t) && (s = !0, p = ["[", "]"]), we(t)) && (c = " [Function" + (t.name ? ": " + t.name : "") + "]");
  return me(t) && (c = " " + RegExp.prototype.toString.call(t)), je(t) && (c = " " + Date.prototype.toUTCString.call(t)), Ae(t) && (c = " " + ce(t)), 0 !== o.length || s && 0 != t.length ? r < 0 ? me(t) ? e.stylize(RegExp.prototype.toString.call(t), "regexp") : e.stylize("[Object]", "special") : (e.seen.push(t), a = s ? function (e, t, r, n, i) {
    for (var o = [], u = 0, f = t.length; u < f; ++u) ke(t, String(u)) ? o.push(se(e, t, r, n, String(u), !0)) : o.push("");

    return i.forEach(function (i) {
      i.match(/^\d+$/) || o.push(se(e, t, r, n, i, !0));
    }), o;
  }(e, t, r, u, o) : o.map(function (n) {
    return se(e, t, r, u, n, s);
  }), e.seen.pop(), function (e, t, r) {
    var n = 0;
    if (e.reduce(function (e, t) {
      return n++, t.indexOf("\n") >= 0 && n++, e + t.replace(/\u001b\[\d\d?m/g, "").length + 1;
    }, 0) > 60) return r[0] + ("" === t ? "" : t + "\n ") + " " + e.join(",\n  ") + " " + r[1];
    return r[0] + t + " " + e.join(", ") + " " + r[1];
  }(a, c, p)) : p[0] + c + p[1];
}

function ce(e) {
  return "[" + Error.prototype.toString.call(e) + "]";
}

function se(e, t, r, n, i, o) {
  var u, f, a;

  if ((a = Object.getOwnPropertyDescriptor(t, i) || {
    value: t[i]
  }).get ? f = a.set ? e.stylize("[Getter/Setter]", "special") : e.stylize("[Getter]", "special") : a.set && (f = e.stylize("[Setter]", "special")), ke(n, i) || (u = "[" + i + "]"), f || (e.seen.indexOf(a.value) < 0 ? (f = le(r) ? ae(e, a.value, null) : ae(e, a.value, r - 1)).indexOf("\n") > -1 && (f = o ? f.split("\n").map(function (e) {
    return "  " + e;
  }).join("\n").substr(2) : "\n" + f.split("\n").map(function (e) {
    return "   " + e;
  }).join("\n")) : f = e.stylize("[Circular]", "special")), be(u)) {
    if (o && i.match(/^\d+$/)) return f;
    (u = JSON.stringify("" + i)).match(/^"([a-zA-Z_][a-zA-Z_0-9]*)"$/) ? (u = u.substr(1, u.length - 2), u = e.stylize(u, "name")) : (u = u.replace(/'/g, "\\'").replace(/\\"/g, '"').replace(/(^"|"$)/g, "'"), u = e.stylize(u, "string"));
  }

  return u + ": " + f;
}

function pe(e) {
  return Array.isArray(e);
}

function ye(e) {
  return "boolean" == typeof e;
}

function le(e) {
  return null === e;
}

function de(e) {
  return "number" == typeof e;
}

function ge(e) {
  return "string" == typeof e;
}

function be(e) {
  return void 0 === e;
}

function me(e) {
  return he(e) && "[object RegExp]" === ve(e);
}

function he(e) {
  return "object" == typeof e && null !== e;
}

function je(e) {
  return he(e) && "[object Date]" === ve(e);
}

function Ae(e) {
  return he(e) && ("[object Error]" === ve(e) || e instanceof Error);
}

function we(e) {
  return "function" == typeof e;
}

function ve(e) {
  return Object.prototype.toString.call(e);
}

function Oe(e) {
  return e < 10 ? "0" + e.toString(10) : e.toString(10);
}

X.debuglog = function (e) {
  if (e = e.toUpperCase(), !re[e]) if (ne.test(e)) {
    var t = Y.pid;

    re[e] = function () {
      var r = X.format.apply(X, arguments);
      console.error("%s %d: %s", e, t, r);
    };
  } else re[e] = function () {};
  return re[e];
}, X.inspect = oe, oe.colors = {
  bold: [1, 22],
  italic: [3, 23],
  underline: [4, 24],
  inverse: [7, 27],
  white: [37, 39],
  grey: [90, 39],
  black: [30, 39],
  blue: [34, 39],
  cyan: [36, 39],
  green: [32, 39],
  magenta: [35, 39],
  red: [31, 39],
  yellow: [33, 39]
}, oe.styles = {
  special: "cyan",
  number: "yellow",
  boolean: "yellow",
  undefined: "grey",
  null: "bold",
  string: "green",
  date: "magenta",
  regexp: "red"
}, X.types = o$2, X.isArray = pe, X.isBoolean = ye, X.isNull = le, X.isNullOrUndefined = function (e) {
  return null == e;
}, X.isNumber = de, X.isString = ge, X.isSymbol = function (e) {
  return "symbol" == typeof e;
}, X.isUndefined = be, X.isRegExp = me, X.types.isRegExp = me, X.isObject = he, X.isDate = je, X.types.isDate = je, X.isError = Ae, X.types.isNativeError = Ae, X.isFunction = we, X.isPrimitive = function (e) {
  return null === e || "boolean" == typeof e || "number" == typeof e || "string" == typeof e || "symbol" == typeof e || void 0 === e;
}, X.isBuffer = i$1;
var Se = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

function Be() {
  var e = new Date(),
      t = [Oe(e.getHours()), Oe(e.getMinutes()), Oe(e.getSeconds())].join(":");
  return [e.getDate(), Se[e.getMonth()], t].join(" ");
}

function ke(e, t) {
  return Object.prototype.hasOwnProperty.call(e, t);
}

X.log = function () {
  console.log("%s - %s", Be(), X.format.apply(X, arguments));
}, X.inherits = t$2, X._extend = function (e, t) {
  if (!t || !he(t)) return e;

  for (var r = Object.keys(t), n = r.length; n--;) e[r[n]] = t[r[n]];

  return e;
};
var Ee = "undefined" != typeof Symbol ? Symbol("util.promisify.custom") : void 0;

function De(e, t) {
  if (!e) {
    var r = new Error("Promise was rejected with a falsy value");
    r.reason = e, e = r;
  }

  return t(e);
}

X.promisify = function (e) {
  if ("function" != typeof e) throw new TypeError('The "original" argument must be of type Function');

  if (Ee && e[Ee]) {
    var t;
    if ("function" != typeof (t = e[Ee])) throw new TypeError('The "util.promisify.custom" argument must be of type Function');
    return Object.defineProperty(t, Ee, {
      value: t,
      enumerable: !1,
      writable: !1,
      configurable: !0
    }), t;
  }

  function t() {
    for (var t, r, n = new Promise(function (e, n) {
      t = e, r = n;
    }), i = [], o = 0; o < arguments.length; o++) i.push(arguments[o]);

    i.push(function (e, n) {
      e ? r(e) : t(n);
    });

    try {
      e.apply(this || Q, i);
    } catch (e) {
      r(e);
    }

    return n;
  }

  return Object.setPrototypeOf(t, Object.getPrototypeOf(e)), Ee && Object.defineProperty(t, Ee, {
    value: t,
    enumerable: !1,
    writable: !1,
    configurable: !0
  }), Object.defineProperties(t, ee(e));
}, X.promisify.custom = Ee, X.callbackify = function (e) {
  if ("function" != typeof e) throw new TypeError('The "original" argument must be of type Function');

  function t() {
    for (var t = [], r = 0; r < arguments.length; r++) t.push(arguments[r]);

    var n = t.pop();
    if ("function" != typeof n) throw new TypeError("The last argument must be of type Function");

    var i = this || Q,
        o = function () {
      return n.apply(i, arguments);
    };

    e.apply(this || Q, t).then(function (e) {
      Y.nextTick(o.bind(null, null, e));
    }, function (e) {
      Y.nextTick(De.bind(null, e, o));
    });
  }

  return Object.setPrototypeOf(t, Object.getPrototypeOf(e)), Object.defineProperties(t, ee(e)), t;
};
export { t$2 as t, X as u };