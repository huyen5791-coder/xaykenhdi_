const http=require('http'),fs=require('fs'),path=require('path');const {chromium}=require('playwright');
const root=__dirname;
const srv=http.createServer((q,r)=>{const p=path.join(root,decodeURIComponent(q.url.split('?')[0]));fs.readFile(p,(e,d)=>{if(e){r.writeHead(404);return r.end();}r.writeHead(200,{'Content-Type':p.endsWith('.js')?'text/javascript':'text/html'});r.end(d);});}).listen(8765);
(async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});const pg=await b.newPage();
pg.on('console',m=>console.log('C:',m.text()));pg.on('pageerror',e=>console.log('E:',e.message));
await pg.goto('http://localhost:8765/index.html');await pg.waitForFunction('window.ready',null,{timeout:60000});
const N=24;fs.mkdirSync('out',{recursive:true});
for(const t of (process.argv[2]||'star,heart,sparkle,arrow,bubble,ring,blob,cube').split(',')){for(let i=0;i<N;i++){const d=await pg.evaluate(([t,i,N])=>render(t,i/N),[t,i,N]);fs.writeFileSync(`out/${t}_${String(i).padStart(2,'0')}.png`,Buffer.from(d.split(',')[1],'base64'));}console.log('done',t);}
await b.close();srv.close();})();
