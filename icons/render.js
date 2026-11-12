const d=require('./node_modules/@iconify-json/fluent-emoji/icons.json');const fs=require('fs');const {chromium}=require('playwright');
const names=process.argv.slice(2);
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:200,height:200}});
fs.mkdirSync('png',{recursive:true});
for(const n of names){let ic=d.icons[n]; if(!ic){ic=d.icons[d.aliases[n].parent];}
 const w=ic.width||d.width||32,h=ic.height||d.height||32;
 const svg=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="200" height="200">${ic.body}</svg>`;
 await p.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
 await p.locator('svg').screenshot({path:`png/${n}.png`,omitBackground:true});}
await b.close();})();
