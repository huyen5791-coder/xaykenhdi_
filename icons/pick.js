const d=require('./node_modules/@iconify-json/fluent-emoji/icons.json');
const want=process.argv.slice(2);
const all=Object.keys(d.icons).concat(Object.keys(d.aliases||{}));
for(const w of want){ console.log(w, all.includes(w)?'OK':'-- '+all.filter(n=>n.includes(w.split('-')[0])).slice(0,8).join(' ')); }
