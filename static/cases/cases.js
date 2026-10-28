// Generated from the real-phone run logs; do not edit by hand.
window.PHONE_CASES = [
 {
  "no": "01",
  "app": "eBay",
  "occasion": "tap-type",
  "query": "wireless headphones",
  "instr": "In eBay as a guest, open the public search box, type \"wireless headphones\", and stop with the public autocomplete search suggestions visible.",
  "frames": [
   "static/cases/01/0.webp",
   "static/cases/01/1.webp",
   "static/cases/01/2.webp"
  ],
  "mask": [],
  "cands": [
   {
    "q": "wireless headphones",
    "app": "eBay",
    "sim": 1.0,
    "sel": true,
    "steps": [
     {
      "a": 1,
      "app": "eBay",
      "label": "Tap the search bar",
      "shared": false
     },
     {
      "a": 2,
      "app": "eBay",
      "label": "Type “wireless headphones”",
      "shared": false
     }
    ]
   },
   {
    "q": "mechanical keyboard",
    "app": "eBay",
    "sim": 0.97,
    "sel": false,
    "steps": [
     {
      "a": 1,
      "app": "eBay",
      "label": "Tap the search bar",
      "shared": true
     },
     {
      "a": 3,
      "app": "eBay",
      "label": "Type “mechanical keyboard”",
      "shared": false
     }
    ]
   },
   {
    "q": "Tokyo",
    "app": "Airbnb",
    "sim": 0.87,
    "sel": false,
    "steps": [
     {
      "a": 1,
      "app": "Airbnb",
      "label": "Tap the search bar",
      "shared": false
     },
     {
      "a": 2,
      "app": "Airbnb",
      "label": "Type “Tokyo”",
      "shared": false
     }
    ]
   }
  ],
  "changed": [],
  "steps": [
   {
    "a": 1,
    "v": 1,
    "app": "eBay",
    "label": "Tap the search bar",
    "tool": "click",
    "text": null,
    "check": "ui_target_match",
    "ok": true,
    "box": [
     44,
     141,
     955,
     202
    ],
    "sharedWith": 1
   },
   {
    "a": 2,
    "v": 1,
    "app": "eBay",
    "label": "Type “wireless headphones”",
    "tool": "type",
    "text": "wireless headphones",
    "check": "keyboard_detected",
    "ok": true,
    "box": null,
    "sharedWith": 0
   }
  ],
  "reused": 2,
  "agent": 0,
  "result": "Search suggestions for “wireless headphones” are on screen.",
  "resultBox": [
   20,
   112,
   980,
   612
  ]
 },
 {
  "no": "02",
  "app": "Airbnb",
  "occasion": "tap-field",
  "query": "Tokyo",
  "instr": "In Airbnb as a guest, open the destination search, type \"Tokyo\", and stop with the public destination suggestions visible.",
  "frames": [
   "static/cases/02/0.webp",
   "static/cases/02/1.webp",
   "static/cases/02/2.webp"
  ],
  "mask": [],
  "cands": [
   {
    "q": "Tokyo",
    "app": "Airbnb",
    "sim": 1.0,
    "sel": true,
    "steps": [
     {
      "a": 1,
      "app": "Airbnb",
      "label": "Tap the search bar",
      "shared": false
     },
     {
      "a": 2,
      "app": "Airbnb",
      "label": "Type “Tokyo”",
      "shared": false
     }
    ]
   },
   {
    "q": "wireless headphones",
    "app": "eBay",
    "sim": 0.87,
    "sel": false,
    "steps": [
     {
      "a": 1,
      "app": "eBay",
      "label": "Tap the search bar",
      "shared": false
     },
     {
      "a": 2,
      "app": "eBay",
      "label": "Type “wireless headphones”",
      "shared": false
     }
    ]
   },
   {
    "q": "mechanical keyboard",
    "app": "eBay",
    "sim": 0.85,
    "sel": false,
    "steps": [
     {
      "a": 1,
      "app": "eBay",
      "label": "Tap the search bar",
      "shared": false
     },
     {
      "a": 3,
      "app": "eBay",
      "label": "Type “mechanical keyboard”",
      "shared": false
     }
    ]
   }
  ],
  "changed": [],
  "steps": [
   {
    "a": 1,
    "v": 1,
    "app": "Airbnb",
    "label": "Tap the search bar",
    "tool": "click",
    "text": null,
    "check": "ui_target_match",
    "ok": true,
    "box": [
     111,
     65,
     888,
     136
    ],
    "sharedWith": 0
   },
   {
    "a": 2,
    "v": 1,
    "app": "Airbnb",
    "label": "Type “Tokyo”",
    "tool": "type",
    "text": "Tokyo",
    "check": "input_target_ui_match",
    "ok": true,
    "box": [
     100,
     263,
     900,
     334
    ],
    "sharedWith": 0
   }
  ],
  "reused": 2,
  "agent": 0,
  "result": "Destination suggestions for “Tokyo” are on screen.",
  "resultBox": [
   20,
   172,
   980,
   612
  ]
 },
 {
  "no": "03",
  "app": "eBay",
  "occasion": "tap-type",
  "query": "mechanical keyboard",
  "instr": "In eBay as a guest, open the public search box, type \"mechanical keyboard\", and stop with the public autocomplete search suggestions visible.",
  "frames": [
   "static/cases/03/0.webp",
   "static/cases/03/1.webp",
   "static/cases/03/2.webp"
  ],
  "mask": [],
  "cands": [
   {
    "q": "mechanical keyboard",
    "app": "eBay",
    "sim": 1.0,
    "sel": true,
    "steps": [
     {
      "a": 1,
      "app": "eBay",
      "label": "Tap the search bar",
      "shared": false
     },
     {
      "a": 3,
      "app": "eBay",
      "label": "Type “mechanical keyboard”",
      "shared": false
     }
    ]
   },
   {
    "q": "wireless headphones",
    "app": "eBay",
    "sim": 0.97,
    "sel": false,
    "steps": [
     {
      "a": 1,
      "app": "eBay",
      "label": "Tap the search bar",
      "shared": true
     },
     {
      "a": 2,
      "app": "eBay",
      "label": "Type “wireless headphones”",
      "shared": false
     }
    ]
   },
   {
    "q": "Tokyo",
    "app": "Airbnb",
    "sim": 0.85,
    "sel": false,
    "steps": [
     {
      "a": 1,
      "app": "Airbnb",
      "label": "Tap the search bar",
      "shared": false
     },
     {
      "a": 2,
      "app": "Airbnb",
      "label": "Type “Tokyo”",
      "shared": false
     }
    ]
   }
  ],
  "changed": [],
  "steps": [
   {
    "a": 1,
    "v": 1,
    "app": "eBay",
    "label": "Tap the search bar",
    "tool": "click",
    "text": null,
    "check": "ui_target_match",
    "ok": true,
    "box": [
     44,
     141,
     955,
     202
    ],
    "sharedWith": 1
   },
   {
    "a": 3,
    "v": 1,
    "app": "eBay",
    "label": "Type “mechanical keyboard”",
    "tool": "type",
    "text": "mechanical keyboard",
    "check": "keyboard_detected",
    "ok": true,
    "box": null,
    "sharedWith": 0
   }
  ],
  "reused": 2,
  "agent": 0,
  "result": "Search suggestions for “mechanical keyboard” are on screen.",
  "resultBox": [
   20,
   112,
   980,
   612
  ]
 },
 {
  "no": "04",
  "app": "Airbnb",
  "occasion": "tap-field",
  "query": "Kyoto",
  "instr": "In Airbnb as a guest, open the destination search, type \"Kyoto\", and stop with the public destination suggestions visible.",
  "frames": [
   "static/cases/04/0.webp",
   "static/cases/04/1.webp",
   "static/cases/04/2.webp"
  ],
  "mask": [],
  "cands": [
   {
    "q": "Kyoto",
    "app": "Airbnb",
    "sim": 1.0,
    "sel": true,
    "steps": [
     {
      "a": 1,
      "app": "Airbnb",
      "label": "Tap the search bar",
      "shared": false
     },
     {
      "a": 3,
      "app": "Airbnb",
      "label": "Type “Kyoto”",
      "shared": false
     }
    ]
   },
   {
    "q": "Tokyo",
    "app": "Airbnb",
    "sim": 0.98,
    "sel": false,
    "steps": [
     {
      "a": 1,
      "app": "Airbnb",
      "label": "Tap the search bar",
      "shared": true
     },
     {
      "a": 2,
      "app": "Airbnb",
      "label": "Type “Tokyo”",
      "shared": false
     }
    ]
   },
   {
    "q": "wireless headphones",
    "app": "eBay",
    "sim": 0.87,
    "sel": false,
    "steps": [
     {
      "a": 1,
      "app": "eBay",
      "label": "Tap the search bar",
      "shared": false
     },
     {
      "a": 2,
      "app": "eBay",
      "label": "Type “wireless headphones”",
      "shared": false
     }
    ]
   }
  ],
  "changed": [],
  "steps": [
   {
    "a": 1,
    "v": 1,
    "app": "Airbnb",
    "label": "Tap the search bar",
    "tool": "click",
    "text": null,
    "check": "ui_target_match",
    "ok": true,
    "box": [
     111,
     65,
     888,
     136
    ],
    "sharedWith": 1
   },
   {
    "a": 3,
    "v": 1,
    "app": "Airbnb",
    "label": "Type “Kyoto”",
    "tool": "type",
    "text": "Kyoto",
    "check": "input_target_ui_match",
    "ok": true,
    "box": [
     100,
     263,
     900,
     334
    ],
    "sharedWith": 0
   }
  ],
  "reused": 2,
  "agent": 0,
  "result": "Destination suggestions for “Kyoto” are on screen.",
  "resultBox": [
   20,
   172,
   980,
   612
  ]
 },
 {
  "no": "05",
  "app": "Airbnb",
  "occasion": "tap-field",
  "query": "Osaka",
  "instr": "In Airbnb as a guest, open the destination search, type \"Osaka\", and stop with the public destination suggestions visible.",
  "frames": [
   "static/cases/05/0.webp",
   "static/cases/05/1.webp",
   "static/cases/05/2.webp"
  ],
  "mask": [],
  "cands": [
   {
    "q": "Osaka",
    "app": "Airbnb",
    "sim": 1.0,
    "sel": true,
    "steps": [
     {
      "a": 1,
      "app": "Airbnb",
      "label": "Tap the search bar",
      "shared": false
     },
     {
      "a": 3,
      "app": "Airbnb",
      "label": "Type “Osaka”",
      "shared": false
     }
    ]
   },
   {
    "q": "Tokyo",
    "app": "Airbnb",
    "sim": 0.98,
    "sel": false,
    "steps": [
     {
      "a": 1,
      "app": "Airbnb",
      "label": "Tap the search bar",
      "shared": true
     },
     {
      "a": 2,
      "app": "Airbnb",
      "label": "Type “Tokyo”",
      "shared": false
     }
    ]
   },
   {
    "q": "Kyoto",
    "app": "Airbnb",
    "sim": 0.97,
    "sel": false,
    "steps": [
     {
      "a": 1,
      "app": "Airbnb",
      "label": "Tap the search bar",
      "shared": true
     },
     {
      "a": 4,
      "app": "Airbnb",
      "label": "Type “Kyoto”",
      "shared": false
     }
    ]
   }
  ],
  "changed": [],
  "steps": [
   {
    "a": 1,
    "v": 1,
    "app": "Airbnb",
    "label": "Tap the search bar",
    "tool": "click",
    "text": null,
    "check": "ui_target_match",
    "ok": true,
    "box": [
     111,
     65,
     888,
     136
    ],
    "sharedWith": 2
   },
   {
    "a": 3,
    "v": 1,
    "app": "Airbnb",
    "label": "Type “Osaka”",
    "tool": "type",
    "text": "Osaka",
    "check": "input_target_ui_match",
    "ok": true,
    "box": [
     100,
     263,
     900,
     334
    ],
    "sharedWith": 0
   }
  ],
  "reused": 2,
  "agent": 0,
  "result": "Destination suggestions for “Osaka” are on screen.",
  "resultBox": [
   20,
   172,
   980,
   612
  ]
 },
 {
  "no": "06",
  "app": "Airbnb",
  "occasion": "tap-field",
  "query": "Sapporo",
  "instr": "In Airbnb as a guest, open the destination search, type \"Sapporo\", and stop with the public destination suggestions visible.",
  "frames": [
   "static/cases/06/0.webp",
   "static/cases/06/1.webp",
   "static/cases/06/2.webp"
  ],
  "mask": [],
  "cands": [
   {
    "q": "Sapporo",
    "app": "Airbnb",
    "sim": 1.0,
    "sel": true,
    "steps": [
     {
      "a": 1,
      "app": "Airbnb",
      "label": "Tap the search bar",
      "shared": false
     },
     {
      "a": 3,
      "app": "Airbnb",
      "label": "Type “Sapporo”",
      "shared": false
     }
    ]
   },
   {
    "q": "Osaka",
    "app": "Airbnb",
    "sim": 0.97,
    "sel": false,
    "steps": [
     {
      "a": 1,
      "app": "Airbnb",
      "label": "Tap the search bar",
      "shared": true
     },
     {
      "a": 4,
      "app": "Airbnb",
      "label": "Type “Osaka”",
      "shared": false
     }
    ]
   },
   {
    "q": "Tokyo",
    "app": "Airbnb",
    "sim": 0.96,
    "sel": false,
    "steps": [
     {
      "a": 1,
      "app": "Airbnb",
      "label": "Tap the search bar",
      "shared": true
     },
     {
      "a": 2,
      "app": "Airbnb",
      "label": "Type “Tokyo”",
      "shared": false
     }
    ]
   }
  ],
  "changed": [],
  "steps": [
   {
    "a": 1,
    "v": 1,
    "app": "Airbnb",
    "label": "Tap the search bar",
    "tool": "click",
    "text": null,
    "check": "ui_target_match",
    "ok": true,
    "box": [
     111,
     65,
     888,
     136
    ],
    "sharedWith": 2
   },
   {
    "a": 3,
    "v": 1,
    "app": "Airbnb",
    "label": "Type “Sapporo”",
    "tool": "type",
    "text": "Sapporo",
    "check": "input_target_ui_match",
    "ok": true,
    "box": [
     100,
     263,
     900,
     334
    ],
    "sharedWith": 0
   }
  ],
  "reused": 2,
  "agent": 0,
  "result": "Destination suggestions for “Sapporo” are on screen.",
  "resultBox": [
   20,
   172,
   980,
   612
  ]
 },
 {
  "no": "07",
  "app": "eBay",
  "occasion": "tap-type",
  "query": "hiking backpack",
  "instr": "In eBay as a guest, open the public search box, type \"hiking backpack\", and stop with the public autocomplete search suggestions visible.",
  "frames": [
   "static/cases/07/0.webp",
   "static/cases/07/1.webp",
   "static/cases/07/2.webp"
  ],
  "mask": [],
  "cands": [
   {
    "q": "hiking backpack",
    "app": "eBay",
    "sim": 1.0,
    "sel": true,
    "steps": [
     {
      "a": 1,
      "app": "eBay",
      "label": "Tap the search bar",
      "shared": false
     },
     {
      "a": 4,
      "app": "eBay",
      "label": "Type “hiking backpack”",
      "shared": false
     }
    ]
   },
   {
    "q": "wireless headphones",
    "app": "eBay",
    "sim": 0.97,
    "sel": false,
    "steps": [
     {
      "a": 1,
      "app": "eBay",
      "label": "Tap the search bar",
      "shared": true
     },
     {
      "a": 2,
      "app": "eBay",
      "label": "Type “wireless headphones”",
      "shared": false
     }
    ]
   },
   {
    "q": "mechanical keyboard",
    "app": "eBay",
    "sim": 0.97,
    "sel": false,
    "steps": [
     {
      "a": 1,
      "app": "eBay",
      "label": "Tap the search bar",
      "shared": true
     },
     {
      "a": 3,
      "app": "eBay",
      "label": "Type “mechanical keyboard”",
      "shared": false
     }
    ]
   }
  ],
  "changed": [],
  "steps": [
   {
    "a": 1,
    "v": 1,
    "app": "eBay",
    "label": "Tap the search bar",
    "tool": "click",
    "text": null,
    "check": "ui_target_match",
    "ok": true,
    "box": [
     44,
     141,
     955,
     202
    ],
    "sharedWith": 2
   },
   {
    "a": 4,
    "v": 1,
    "app": "eBay",
    "label": "Type “hiking backpack”",
    "tool": "type",
    "text": "hiking backpack",
    "check": "keyboard_detected",
    "ok": true,
    "box": null,
    "sharedWith": 0
   }
  ],
  "reused": 2,
  "agent": 0,
  "result": "Search suggestions for “hiking backpack” are on screen.",
  "resultBox": [
   20,
   112,
   980,
   612
  ]
 },
 {
  "no": "08",
  "app": "eBay",
  "occasion": "tap-type",
  "query": "digital camera",
  "instr": "In eBay as a guest, open the public search box, type \"digital camera\", and stop with the public autocomplete search suggestions visible.",
  "frames": [
   "static/cases/08/0.webp",
   "static/cases/08/1.webp",
   "static/cases/08/2.webp"
  ],
  "mask": [],
  "cands": [
   {
    "q": "digital camera",
    "app": "eBay",
    "sim": 1.0,
    "sel": true,
    "steps": [
     {
      "a": 3,
      "app": "eBay",
      "label": "Tap the search bar",
      "shared": false
     },
     {
      "a": 4,
      "app": "eBay",
      "label": "Type “digital camera”",
      "shared": false
     }
    ]
   },
   {
    "q": "wireless headphones",
    "app": "eBay",
    "sim": 0.97,
    "sel": false,
    "steps": [
     {
      "a": 1,
      "app": "eBay",
      "label": "Tap the search bar",
      "shared": false
     },
     {
      "a": 2,
      "app": "eBay",
      "label": "Type “wireless headphones”",
      "shared": false
     }
    ]
   },
   {
    "q": "mechanical keyboard",
    "app": "eBay",
    "sim": 0.97,
    "sel": false,
    "steps": [
     {
      "a": 1,
      "app": "eBay",
      "label": "Tap the search bar",
      "shared": false
     },
     {
      "a": 5,
      "app": "eBay",
      "label": "Type “mechanical keyboard”",
      "shared": false
     }
    ]
   }
  ],
  "changed": [],
  "steps": [
   {
    "a": 3,
    "v": 1,
    "app": "eBay",
    "label": "Tap the search bar",
    "tool": "click",
    "text": null,
    "check": "ui_target_match",
    "ok": true,
    "box": [
     44,
     141,
     955,
     202
    ],
    "sharedWith": 0
   },
   {
    "a": 4,
    "v": 1,
    "app": "eBay",
    "label": "Type “digital camera”",
    "tool": "type",
    "text": "digital camera",
    "check": "keyboard_detected",
    "ok": true,
    "box": null,
    "sharedWith": 0
   }
  ],
  "reused": 2,
  "agent": 0,
  "result": "Search suggestions for “digital camera” are on screen.",
  "resultBox": [
   20,
   112,
   980,
   612
  ]
 },
 {
  "no": "09",
  "app": "eBay",
  "occasion": "tap-type",
  "query": "running shoes",
  "instr": "In eBay as a guest, open the public search box, type \"running shoes\", and stop with the public autocomplete search suggestions visible.",
  "frames": [
   "static/cases/09/0.webp",
   "static/cases/09/1.webp",
   "static/cases/09/2.webp"
  ],
  "mask": [],
  "cands": [
   {
    "q": "running shoes",
    "app": "eBay",
    "sim": 1.0,
    "sel": true,
    "steps": [
     {
      "a": 1,
      "app": "eBay",
      "label": "Tap the search bar",
      "shared": false
     },
     {
      "a": 3,
      "app": "eBay",
      "label": "Type “running shoes”",
      "shared": false
     }
    ]
   },
   {
    "q": "hiking backpack",
    "app": "eBay",
    "sim": 0.97,
    "sel": false,
    "steps": [
     {
      "a": 1,
      "app": "eBay",
      "label": "Tap the search bar",
      "shared": true
     },
     {
      "a": 7,
      "app": "eBay",
      "label": "Type “hiking backpack”",
      "shared": false
     }
    ]
   },
   {
    "q": "wireless headphones",
    "app": "eBay",
    "sim": 0.97,
    "sel": false,
    "steps": [
     {
      "a": 1,
      "app": "eBay",
      "label": "Tap the search bar",
      "shared": true
     },
     {
      "a": 2,
      "app": "eBay",
      "label": "Type “wireless headphones”",
      "shared": false
     }
    ]
   }
  ],
  "changed": [],
  "steps": [
   {
    "a": 1,
    "v": 1,
    "app": "eBay",
    "label": "Tap the search bar",
    "tool": "click",
    "text": null,
    "check": "ui_target_match",
    "ok": true,
    "box": [
     44,
     141,
     955,
     202
    ],
    "sharedWith": 2
   },
   {
    "a": 3,
    "v": 1,
    "app": "eBay",
    "label": "Type “running shoes”",
    "tool": "type",
    "text": "running shoes",
    "check": "keyboard_detected",
    "ok": true,
    "box": null,
    "sharedWith": 0
   }
  ],
  "reused": 2,
  "agent": 0,
  "result": "Search suggestions for “running shoes” are on screen.",
  "resultBox": [
   20,
   112,
   980,
   612
  ]
 },
 {
  "no": "10",
  "app": "Airbnb",
  "occasion": "tap-field",
  "query": "Nagoya",
  "instr": "In Airbnb as a guest, open the destination search, type \"Nagoya\", and stop with the public destination suggestions visible.",
  "frames": [
   "static/cases/10/0.webp",
   "static/cases/10/1.webp",
   "static/cases/10/2.webp"
  ],
  "mask": [],
  "cands": [
   {
    "q": "Nagoya",
    "app": "Airbnb",
    "sim": 1.0,
    "sel": true,
    "steps": [
     {
      "a": 1,
      "app": "Airbnb",
      "label": "Tap the search bar",
      "shared": false
     },
     {
      "a": 6,
      "app": "Airbnb",
      "label": "Type “Nagoya”",
      "shared": false
     }
    ]
   },
   {
    "q": "Osaka",
    "app": "Airbnb",
    "sim": 0.97,
    "sel": false,
    "steps": [
     {
      "a": 1,
      "app": "Airbnb",
      "label": "Tap the search bar",
      "shared": true
     },
     {
      "a": 4,
      "app": "Airbnb",
      "label": "Type “Osaka”",
      "shared": false
     }
    ]
   },
   {
    "q": "Tokyo",
    "app": "Airbnb",
    "sim": 0.96,
    "sel": false,
    "steps": [
     {
      "a": 1,
      "app": "Airbnb",
      "label": "Tap the search bar",
      "shared": true
     },
     {
      "a": 2,
      "app": "Airbnb",
      "label": "Type “Tokyo”",
      "shared": false
     }
    ]
   }
  ],
  "changed": [],
  "steps": [
   {
    "a": 1,
    "v": 1,
    "app": "Airbnb",
    "label": "Tap the search bar",
    "tool": "click",
    "text": null,
    "check": "ui_target_match",
    "ok": true,
    "box": [
     111,
     65,
     888,
     136
    ],
    "sharedWith": 2
   },
   {
    "a": 6,
    "v": 1,
    "app": "Airbnb",
    "label": "Type “Nagoya”",
    "tool": "type",
    "text": "Nagoya",
    "check": "input_target_ui_match",
    "ok": true,
    "box": [
     100,
     263,
     900,
     334
    ],
    "sharedWith": 0
   }
  ],
  "reused": 2,
  "agent": 0,
  "result": "Destination suggestions for “Nagoya” are on screen.",
  "resultBox": [
   20,
   172,
   980,
   612
  ]
 },
 {
  "no": "11",
  "app": "YouTube",
  "occasion": "type-enter",
  "query": "aurora borealis",
  "instr": "In YouTube, the empty text-search input is already open and focused. Starting from this prepared input field, type \"aurora borealis\", submit the search by pressing the Enter system button (not by tapping the keyboard), and stop when public video search results are visible.",
  "frames": [
   "static/cases/11/0.webp",
   "static/cases/11/1.webp",
   "static/cases/11/2.webp"
  ],
  "mask": [
   [
    0,
    119,
    1000,
    621
   ]
  ],
  "cands": [
   {
    "q": "aurora borealis",
    "app": "YouTube",
    "sim": 1.0,
    "sel": true,
    "steps": [
     {
      "a": 1,
      "app": "YouTube",
      "label": "Type “aurora borealis”",
      "shared": false
     },
     {
      "a": 1,
      "app": "System",
      "label": "Press Enter",
      "shared": false
     }
    ]
   },
   {
    "q": "mechanical keyboard",
    "app": "eBay",
    "sim": 0.89,
    "sel": false,
    "steps": [
     {
      "a": 1,
      "app": "eBay",
      "label": "Tap the search bar",
      "shared": false
     },
     {
      "a": 6,
      "app": "eBay",
      "label": "Type “mechanical keyboard”",
      "shared": false
     }
    ]
   },
   {
    "q": "digital camera",
    "app": "eBay",
    "sim": 0.89,
    "sel": false,
    "steps": [
     {
      "a": 4,
      "app": "eBay",
      "label": "Tap the search bar",
      "shared": false
     },
     {
      "a": 5,
      "app": "eBay",
      "label": "Type “digital camera”",
      "shared": false
     }
    ]
   }
  ],
  "changed": [],
  "steps": [
   {
    "a": 1,
    "v": 1,
    "app": "YouTube",
    "label": "Type “aurora borealis”",
    "tool": "type",
    "text": "aurora borealis",
    "check": "keyboard_detected",
    "ok": true,
    "box": null,
    "sharedWith": 0
   },
   {
    "a": 1,
    "v": 1,
    "app": "System",
    "label": "Press Enter",
    "tool": "system_button",
    "text": null,
    "check": "non_point_action",
    "ok": true,
    "box": null,
    "sharedWith": 0
   }
  ],
  "reused": 2,
  "agent": 0,
  "result": "Video results for “aurora borealis” are on screen.",
  "resultBox": [
   10,
   106,
   990,
   930
  ]
 }
];
