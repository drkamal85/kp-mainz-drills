// Nightly Motion snapshot → comms/motion-snapshot.json
// Read by the Mentor chat (which cannot reach api.usemotion.com directly).
const https=require('https');
const fs=require('fs');
const KEY=process.env.MOTION_API_KEY;
const P='pr_N8Dk2zfVrLDQi7d1jH1Dq3';
if(!KEY){console.error('MOTION_API_KEY missing');process.exit(1);}

const get=p=>new Promise((res,rej)=>{
  const r=https.request({hostname:'api.usemotion.com',path:'/v1'+p,method:'GET',
    headers:{'X-API-Key':KEY}},resp=>{let d='';resp.on('data',c=>d+=c);
    resp.on('end',()=>{try{res(JSON.parse(d))}catch(e){res({})}})});
  r.on('error',rej);r.end();});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const TODAY=new Date().toISOString().slice(0,10);

const level=n=>{const m=n.match(/\bR([1-5])$/);return m?'R'+m[1]:null;};
const isStudy=n=>n.startsWith('Study:');
const topicOf=n=>n.replace(/^Study:\s*/,'').replace(/^Review:\s*/,'').replace(/\s*R[1-5]$/,'').trim();

(async()=>{
  let open=[],c=null;
  do{const d=await get(`/tasks?projectId=${P}${c?'&cursor='+c:''}`);
     open=open.concat(d.tasks||[]);c=d.meta?.nextCursor||null;await sleep(380);}while(c);
  let done=[],c2=null;
  do{const d=await get(`/tasks?projectId=${P}&status=Completed${c2?'&cursor='+c2:''}`);
     done=done.concat(d.tasks||[]);c2=d.meta?.nextCursor||null;await sleep(380);}while(c2);

  const overdue=open.filter(t=>t.dueDate&&t.dueDate.slice(0,10)<TODAY);
  const flaggedT=open.filter(t=>t.schedulingIssue||!t.scheduledStart);

  // ── workstreams ──
  const topics=new Set([...open,...done].map(t=>topicOf(t.name)).filter(Boolean));
  const studiedTopics=new Set(done.filter(t=>isStudy(t.name)).map(t=>topicOf(t.name)));
  const r1Done=new Set(done.filter(t=>level(t.name)==='R1').map(t=>topicOf(t.name)));

  const cnt=(arr,fn)=>arr.filter(fn).length;
  const ws={
    A_coverage:{
      topicsTotal:topics.size,
      studied:studiedTopics.size,
      studyOpen:cnt(open,t=>isStudy(t.name)),
      r1Built:r1Done.size,
      r1Open:cnt(open,t=>level(t.name)==='R1')
    },
    B_r5:{
      open:cnt(open,t=>level(t.name)==='R5'||/R5-Pilot/i.test(t.name)),
      completed:cnt(done,t=>level(t.name)==='R5'||/R5-Pilot/i.test(t.name)),
      pilot:[...open,...done].filter(t=>/cholezystitis/i.test(t.name)&&/R5/i.test(t.name))
        .map(t=>({name:t.name,dueDate:t.dueDate?.slice(0,10),completed:!!t.completed}))
    },
    C_akte:{
      open:cnt(open,t=>/Akte-Sim/i.test(t.name)),
      completed:cnt(done,t=>/Akte-Sim/i.test(t.name)),
      sessions:[...open,...done].filter(t=>/Akte-Sim/i.test(t.name))
        .map(t=>({name:t.name,dueDate:t.dueDate?.slice(0,10),completed:!!t.completed}))
        .sort((a,b)=>(a.dueDate||'').localeCompare(b.dueDate||''))
    },
    D_bildsprint:{
      open:cnt(open,t=>/Drill|Bild|EKG|BGA|Sono|Echo|EEG|R(ö|oe)ntgen/i.test(t.name)),
      completed:cnt(done,t=>/Drill|Bild|EKG|BGA|Sono|Echo|EEG|R(ö|oe)ntgen/i.test(t.name)),
      note:'Drill tasks live as komplett library files, not Motion tasks'
    }
  };

  // ── level totals ──
  const byLevel={};
  ['R1','R2','R3','R4','R5'].forEach(L=>{
    byLevel[L]={open:cnt(open,t=>level(t.name)===L),completed:cnt(done,t=>level(t.name)===L)};
  });

  // ── next checkpoint ──
  const cps=open.filter(t=>/CHECKPOINT/i.test(t.name)&&t.dueDate)
    .sort((a,b)=>a.dueDate.localeCompare(b.dueDate));
  const nextCheckpoint=cps.length?{name:cps[0].name,dueDate:cps[0].dueDate.slice(0,10)}:null;

  // ── upcoming 14 days ──
  const in14=new Date(Date.now()+14*864e5).toISOString().slice(0,10);
  const upcoming=open.filter(t=>{const d=t.dueDate?.slice(0,10);return d&&d>=TODAY&&d<=in14;})
    .sort((a,b)=>a.dueDate.localeCompare(b.dueDate))
    .map(t=>({name:t.name,dueDate:t.dueDate.slice(0,10),duration:t.duration||0}));

  const snap={
    generatedAt:new Date().toISOString(),
    totals:{open:open.length,completed:done.length,overdue:overdue.length,schedulingIssues:flaggedT.length},
    byLevel,
    byWorkstream:ws,
    flagged:flaggedT.slice(0,60).map(t=>({name:t.name,dueDate:t.dueDate?.slice(0,10)||null,
      schedulingIssue:!!t.schedulingIssue,scheduledStart:t.scheduledStart||null})),
    overdue:overdue.map(t=>({name:t.name,dueDate:t.dueDate.slice(0,10)})),
    upcoming14d:upcoming,
    nextCheckpoint
  };

  fs.mkdirSync('comms',{recursive:true});
  fs.writeFileSync('comms/motion-snapshot.json',JSON.stringify(snap,null,2));
  console.log(`open ${open.length} · completed ${done.length} · overdue ${overdue.length} · flagged ${flaggedT.length}`);
  console.log('written: comms/motion-snapshot.json');
})();
