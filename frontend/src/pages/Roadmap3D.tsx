// src/pages/Roadmap3D.tsx  v6.1
// Changes from v6.0:
// - Removed "scroll or drag bar" pill
// - Removed Pin feature entirely
// - Added "← Dashboard" back button top-left (below navbar)

import { useEffect, useRef, useState, useCallback } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import Navbar from '../components/Navbar'
import FoxMascot from '../components/FoxMascot'
import { generateRoadmap } from '../api/pathforge'
import { loadAnalysis } from '../hooks/useAnalysisStore'
import { useAuth } from '../context/AuthContext'
import type { RoadmapTimeline, RoadmapNode } from '../api/pathforge'

type Resource = { label: string; url: string; free: boolean; type?: 'course'|'dataset'|'docs'|'video' }

function backendToResource(r: {title:string; url:string; type:string; platform:string}): Resource {
  let displayType: Resource['type'] = 'course'
  const u = r.url.toLowerCase()
  const p = (r.platform ?? '').toLowerCase()
  if (u.includes('youtube.com') || p.includes('youtube')) displayType = 'video'
  else if (
    u.includes('/docs') || u.includes('/doc/') || u.includes('readthedocs') ||
    u.includes('documentation') || u.includes('.org/en') || p.includes('docs') ||
    u.includes('manual') || u.includes('reference')
  ) displayType = 'docs'
  else if (
    u.includes('kaggle.com/datasets') || u.includes('archive.ics') ||
    u.includes('paperswithcode.com/datasets') || u.includes('opendata') ||
    u.includes('huggingface.co/datasets') || u.includes('registry.opendata')
  ) displayType = 'dataset'
  return { label: r.title, url: r.url, free: r.type === 'free' || r.type === 'freemium', type: displayType }
}

function getResources(node: RoadmapNode): Resource[] {
  if (node.resources && node.resources.length > 0) {
    return node.resources.map(backendToResource).slice(0, 4)
  }
  return []
}

const TYPE_ICON: Record<string, string> = { course: '🎓', dataset: '📊', docs: '📖', video: '▶' }

const PC = {
  high:   { border: '#ef4444', bg: 'rgba(239,68,68,0.14)',   glow: 'rgba(239,68,68,0.4)',   text: '#fca5a5', ring: 'rgba(239,68,68,0.45)'   },
  medium: { border: '#f59e0b', bg: 'rgba(245,158,11,0.14)',  glow: 'rgba(245,158,11,0.4)',  text: '#fcd34d', ring: 'rgba(245,158,11,0.45)'  },
  low:    { border: '#6b7280', bg: 'rgba(107,114,128,0.1)',  glow: 'rgba(107,114,128,0.25)',text: '#9ca3af', ring: 'rgba(107,114,128,0.3)'  },
}

const VW = 3400
const VH = 420
const PATH_Y = VH * 0.5   // perfectly centred horizontal line

function getPathPoint(t: number) {
  return { x: VW * 0.02 + t * (VW * 0.96), y: PATH_Y }
}

function nodeT(i: number, n: number) { return n <= 1 ? 0.45 : 0.07 + (i/(n-1))*0.78 }

function drawRoad(canvas: HTMLCanvasElement, nodes: RoadmapNode[]) {
  const ctx = canvas.getContext('2d'); if (!ctx) return
  canvas.width = VW; canvas.height = VH; ctx.clearRect(0,0,VW,VH)

  const x0 = VW * 0.02, x1 = VW * 0.98, y = PATH_Y

  // Road base layers
  const road = (w:number, style:string, blur=0, alpha=1) => {
    ctx.save(); ctx.globalAlpha=alpha
    if (blur) ctx.filter=`blur(${blur}px)`
    ctx.beginPath(); ctx.moveTo(x0,y); ctx.lineTo(x1,y)
    ctx.strokeStyle=style; ctx.lineWidth=w; ctx.lineCap='round'; ctx.stroke(); ctx.restore()
  }
  road(50,'rgba(0,0,0,0.9)'); road(34,'#070915'); road(38,'rgba(124,58,237,0.13)',4)

  const n = nodes.length
  if (n > 0) {
    const fm = nodes.findIndex(nd=>nd.priority!=='high')
    const fl = nodes.findIndex(nd=>nd.priority==='low')
    const hEnd = fm>0 ? nodeT(fm-1,n) : nodeT(n-1,n)
    const mEnd = fl>0 ? nodeT(fl-1,n) : hEnd

    const seg = (tA:number, tB:number, col:string) => {
      if (tA >= tB) return
      const xa = x0 + tA*(x1-x0), xb = x0 + tB*(x1-x0)
      ctx.save()
      ctx.beginPath(); ctx.moveTo(xa,y); ctx.lineTo(xb,y)
      ctx.strokeStyle=col; ctx.lineWidth=5; ctx.lineCap='round'; ctx.stroke()
      ctx.filter='blur(10px)'; ctx.globalAlpha=0.35; ctx.lineWidth=18; ctx.strokeStyle=col; ctx.stroke()
      ctx.restore()
    }
    seg(0,    hEnd, '#ef4444')
    seg(hEnd, mEnd, '#f59e0b')
    seg(mEnd, 1,    '#8b5cf6')
  } else {
    road(5,'rgba(139,92,246,0.4)')
  }
}

export default function Roadmap3D() {
  const navigate   = useNavigate()
  const [params]   = useSearchParams()
  const { user }   = useAuth()

  const [timeline,  setTimeline]  = useState<RoadmapTimeline|null>(null)
  const [loading,   setLoading]   = useState(true)
  const [error,     setError]     = useState<string|null>(null)
  const [selected,  setSelected]  = useState<RoadmapNode|null>(null)
  const [hovered,   setHovered]   = useState<{node:RoadmapNode;x:number;y:number}|null>(null)
  const [doneIds,   setDoneIds]   = useState<Set<string>>(new Set())
  const [scrollPct, setScrollPct] = useState(0)
  const [tab,       setTab]       = useState<'info'|'links'>('info')

  const containerRef = useRef<HTMLDivElement>(null)
  const canvasRef    = useRef<HTMLCanvasElement>(null)
  const scrubRef     = useRef<HTMLDivElement>(null)
  const panX=useRef(0),panY=useRef(0),tPanX=useRef(0),tPanY=useRef(0)
  const [pan,setPan] = useState({x:0,y:0})
  const animRef=useRef<number>(0),scrollRef=useRef(0),nodesRef=useRef<RoadmapNode[]>([])

  const goTo = useCallback((pct:number)=>{
    const t=Math.max(0,Math.min(1,pct))
    scrollRef.current=t; setScrollPct(t)
    const iw=window.innerWidth,ih=window.innerHeight
    const pt=getPathPoint(t)
    tPanX.current=pt.x-iw*0.42; tPanY.current=pt.y-ih*0.5
  },[])

  // Load data
  useEffect(()=>{
    async function load(){
      try{
        let payload:any=null
        const id=params.get('id')
        if(id&&user?.uid){
          const s=await loadAnalysis(user.uid,id)
          if(!s){setError('Analysis not found.');setLoading(false);return}
          payload={gapSkills:s.gapSkills,matchedSkills:(s as any).matchedSkills??[],targetRole:s.targetRole,matchScore:s.matchScore,candidateName:user.displayName||'Candidate'}
        } else {
          const raw=sessionStorage.getItem('analysisResult')
          if(!raw){setError('No analysis data. Run an analysis first.');setLoading(false);return}
          payload=JSON.parse(raw)
          if(!payload?.gapSkills?.length){setError('No gap skills found. Please run an analysis first.');setLoading(false);return}
        }
        const result=await generateRoadmap(payload)
        if(!result?.nodes?.length){setError('Roadmap is empty. Is the backend running at port 8000?');setLoading(false);return}
        nodesRef.current=result.nodes; setTimeline(result)
        const iw=window.innerWidth,ih=window.innerHeight
        const s0=getPathPoint(nodeT(0,result.nodes.length))
        panX.current=s0.x-iw*0.22; panY.current=s0.y-ih*0.5
        tPanX.current=panX.current; tPanY.current=panY.current
        setPan({x:panX.current,y:panY.current})
        setLoading(false)
      } catch(e){setError(`Failed: ${e instanceof Error?e.message:'Unknown error'}`);setLoading(false)}
    }
    load()
  },[params,user])

  const redraw=useCallback(()=>{if(canvasRef.current&&nodesRef.current.length)drawRoad(canvasRef.current,nodesRef.current)},[])
  useEffect(()=>{redraw()},[timeline,redraw])

  // Lerp animation
  useEffect(()=>{
    const loop=()=>{
      const dx=tPanX.current-panX.current,dy=tPanY.current-panY.current
      if(Math.abs(dx)>0.4||Math.abs(dy)>0.4){panX.current+=dx*0.1;panY.current+=dy*0.1;setPan({x:panX.current,y:panY.current})}
      animRef.current=requestAnimationFrame(loop)
    }
    animRef.current=requestAnimationFrame(loop)
    return ()=>cancelAnimationFrame(animRef.current)
  },[])

  // Wheel scroll
  useEffect(()=>{
    if(loading)return
    const el=containerRef.current;if(!el)return
    const fn=(e:WheelEvent)=>{e.preventDefault();goTo(scrollRef.current+e.deltaY/600)}
    el.addEventListener('wheel',fn,{passive:false})
    return ()=>el.removeEventListener('wheel',fn)
  },[loading,goTo])

  // Touch scroll
  useEffect(()=>{
    if(loading)return
    const el=containerRef.current;if(!el)return
    let lx=0,ly=0
    const ts=(e:TouchEvent)=>{lx=e.touches[0].clientX;ly=e.touches[0].clientY}
    const tm=(e:TouchEvent)=>{
      e.preventDefault()
      const dx=lx-e.touches[0].clientX,dy=ly-e.touches[0].clientY
      lx=e.touches[0].clientX;ly=e.touches[0].clientY
      goTo(scrollRef.current+(Math.abs(dx)>=Math.abs(dy)?dx:dy)/450)
    }
    el.addEventListener('touchstart',ts);el.addEventListener('touchmove',tm,{passive:false})
    return ()=>{el.removeEventListener('touchstart',ts);el.removeEventListener('touchmove',tm)}
  },[loading,goTo])

  // Draggable scrubber
  useEffect(()=>{
    if(loading)return
    const track=scrubRef.current;if(!track)return
    let dragging=false
    const getPct=(e:MouseEvent)=>{const r=track.getBoundingClientRect();return Math.max(0,Math.min(1,(e.clientX-r.left)/r.width))}
    const onDown=(e:MouseEvent)=>{dragging=true;goTo(getPct(e));e.preventDefault()}
    const onMove=(e:MouseEvent)=>{if(dragging){goTo(getPct(e));e.preventDefault()}}
    const onUp=()=>{dragging=false}
    track.addEventListener('mousedown',onDown)
    window.addEventListener('mousemove',onMove)
    window.addEventListener('mouseup',onUp)
    return ()=>{track.removeEventListener('mousedown',onDown);window.removeEventListener('mousemove',onMove);window.removeEventListener('mouseup',onUp)}
  },[loading,goTo])

  function toggleDone(id:string){setDoneIds(p=>{const s=new Set(p);s.has(id)?s.delete(id):s.add(id);return s})}

  if(loading) return (
    <div style={{minHeight:'100vh',background:'#06080f',display:'flex',alignItems:'center',justifyContent:'center',flexDirection:'column',gap:24}}>
      <link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&family=IBM+Plex+Mono:wght@500&display=swap" rel="stylesheet"/>
      <div style={{position:'relative'}}>
        <div style={{width:52,height:52,border:'2px solid rgba(139,92,246,0.15)',borderTopColor:'#8b5cf6',borderRadius:'50%',animation:'spin 1s linear infinite'}}/>
        <div style={{position:'absolute',inset:8,border:'2px solid rgba(6,182,212,0.12)',borderBottomColor:'#06b6d4',borderRadius:'50%',animation:'spin 1.6s linear infinite reverse'}}/>
      </div>
      <div style={{fontFamily:"'Syne',sans-serif",fontSize:14,color:'#374151',letterSpacing:1}}>Building your roadmap…</div>
      <FoxMascot size={100}/>
      <style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style>
    </div>
  )

  if(error) return (
    <div style={{minHeight:'100vh',background:'#06080f',display:'flex',alignItems:'center',justifyContent:'center'}}>
      <link href="https://fonts.googleapis.com/css2?family=Syne:wght@700&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet"/>
      <div style={{background:'rgba(239,68,68,0.05)',border:'1px solid rgba(239,68,68,0.2)',borderRadius:16,padding:'36px 44px',textAlign:'center',maxWidth:500}}>
        <p style={{color:'#ef4444',marginBottom:24,lineHeight:1.6,fontSize:14}}>{error}</p>
        <div style={{display:'flex',gap:10,justifyContent:'center'}}>
          <button onClick={()=>navigate('/upload')} style={{background:'rgba(239,68,68,0.09)',border:'1px solid rgba(239,68,68,0.22)',color:'#ef4444',padding:'9px 20px',borderRadius:8,cursor:'pointer',fontSize:13}}>New Analysis</button>
          <button onClick={()=>navigate('/dashboard')} style={{background:'rgba(255,255,255,0.03)',border:'1px solid rgba(255,255,255,0.07)',color:'#6b7280',padding:'9px 20px',borderRadius:8,cursor:'pointer',fontSize:13}}>Dashboard</button>
        </div>
      </div>
    </div>
  )

  if(!timeline) return null
  const {nodes,total_weeks,candidate_name,target_role,match_score}=timeline
  const doneCount=doneIds.size,pct=nodes.length>0?Math.round(doneCount/nodes.length*100):0
  const highN=nodes.filter(n=>n.priority==='high'&&!n.is_prerequisite_only).length

  return (
    <div style={{height:'100vh',background:'#06080f',display:'flex',flexDirection:'column',overflow:'hidden'}}>
      <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet"/>
      <Navbar/>

      {/* TOP BAR */}
      <div style={{position:'fixed',top:64,left:0,right:0,zIndex:20,background:'rgba(6,8,15,0.97)',borderBottom:'1px solid rgba(255,255,255,0.04)',backdropFilter:'blur(12px)'}}>
        {/* Row 1 */}
        <div style={{padding:'10px 24px 0',display:'flex',alignItems:'center',justifyContent:'space-between',gap:16}}>
          {/* Back button — top-left */}
          <button
            onClick={()=>navigate('/dashboard')}
            style={{background:'transparent',border:'none',color:'#4b5563',fontSize:13,cursor:'pointer',display:'flex',alignItems:'center',gap:5,padding:'4px 0',fontFamily:"'DM Sans',sans-serif",transition:'color 0.15s',flexShrink:0}}
            onMouseEnter={e=>(e.currentTarget.style.color='#9ca3af')}
            onMouseLeave={e=>(e.currentTarget.style.color='#4b5563')}
          >
            ← Dashboard
          </button>

          {/* Centre title */}
          <div style={{textAlign:'center',flex:1}}>
            <div style={{fontFamily:"'Syne',sans-serif",fontSize:16,fontWeight:800,color:'#f8fafc',letterSpacing:'-0.3px'}}>{candidate_name}'s Roadmap</div>
            <div style={{fontSize:10,color:'#374151',fontFamily:"'IBM Plex Mono',monospace",marginTop:1}}>{target_role} · {nodes.length} skills · {total_weeks}w · {match_score}% match</div>
          </div>

          {/* Progress bar — right */}
          <div style={{display:'flex',alignItems:'center',gap:8,minWidth:140,flexShrink:0}}>
            <div style={{flex:1,height:4,background:'rgba(255,255,255,0.05)',borderRadius:2,overflow:'hidden'}}>
              <div style={{height:'100%',width:`${pct}%`,background:'linear-gradient(90deg,#10b981,#8b5cf6)',borderRadius:2,transition:'width 0.5s'}}/>
            </div>
            <span style={{fontSize:10,color:'#10b981',fontFamily:"'IBM Plex Mono',monospace",whiteSpace:'nowrap'}}>{pct}%</span>
          </div>
        </div>

        {/* Row 2 — pills only (no pin, no scroll hint) */}
        <div style={{padding:'7px 24px 9px',display:'flex',alignItems:'center',gap:7,flexWrap:'wrap'}}>
          <Pill color="#34d399" bg="rgba(16,185,129,0.07)">{doneCount}/{nodes.length} done</Pill>
          <Pill color="#fca5a5" bg="rgba(239,68,68,0.07)">{highN} urgent</Pill>
          <div style={{flex:1}}/>
        </div>
      </div>

      {/* SCENE */}
      <div ref={containerRef} style={{flex:1,marginTop:110,position:'relative',overflow:'hidden',cursor:'ew-resize'}}>
        {/* Glows */}
        <div style={{position:'absolute',width:800,height:350,borderRadius:'50%',background:'radial-gradient(circle,rgba(124,58,237,0.07) 0%,transparent 70%)',top:'5%',left:'-5%',filter:'blur(100px)',pointerEvents:'none',zIndex:1}}/>
        <div style={{position:'absolute',width:500,height:250,borderRadius:'50%',background:'radial-gradient(circle,rgba(6,182,212,0.05) 0%,transparent 70%)',bottom:'10%',right:0,filter:'blur(80px)',pointerEvents:'none',zIndex:1}}/>
        <div style={{position:'absolute',width:'220%',height:'200%',left:'-60%',top:'15%',transform:'rotateX(62deg)',transformOrigin:'center top',backgroundImage:'linear-gradient(rgba(124,58,237,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(124,58,237,0.03) 1px,transparent 1px)',backgroundSize:'58px 58px',pointerEvents:'none',zIndex:0}}/>

        {/* Virtual world */}
        <div style={{position:'absolute',left:-pan.x,top:-pan.y,width:VW,height:VH,zIndex:2}}>
          <canvas ref={canvasRef} style={{position:'absolute',left:0,top:0,width:VW,height:VH,pointerEvents:'none'}}/>

          {nodes.map((node,idx)=>{
            const t=nodeT(idx,nodes.length),pos=getPathPoint(t)
            const c=PC[node.priority],isDone=doneIds.has(node.id),isSel=selected?.id===node.id,isPrq=node.is_prerequisite_only
            const sz=node.priority==='high'?60:node.priority==='medium'?52:46
            return (
              <div key={node.id}
                style={{position:'absolute',left:pos.x-sz/2,top:pos.y-sz/2,zIndex:node.priority==='high'?8:6,opacity:isPrq?0.38:1,cursor:'pointer',animation:`nfloat ${4.5+idx*0.22}s ${idx*0.14}s ease-in-out infinite`}}
                onClick={()=>{setSelected(p=>p?.id===node.id?null:node);setTab('info')}}
                onMouseEnter={e=>{const r=(e.currentTarget as HTMLElement).getBoundingClientRect();setHovered({node,x:r.left+sz/2,y:r.top-8})}}
                onMouseLeave={()=>setHovered(null)}
              >
                {!isDone&&!isPrq&&<div style={{position:'absolute',width:sz+20,height:sz+20,top:-10,left:-10,borderRadius:'50%',border:`1px solid ${c.ring}`,animation:'rpulse 2.5s ease-out infinite'}}/>}
                {isSel&&<div style={{position:'absolute',width:sz+36,height:sz+36,top:-18,left:-18,borderRadius:'50%',border:'1px solid rgba(255,255,255,0.12)',animation:'rpulse 2s ease-out infinite'}}/>}
                <div style={{width:sz,height:sz,borderRadius:'50%',background:isDone?'rgba(16,185,129,0.14)':c.bg,border:`${isSel?2.5:1.5}px solid ${isDone?'#10b981':isSel?'rgba(255,255,255,0.55)':c.border}`,boxShadow:isPrq?'none':isDone?'0 0 16px rgba(16,185,129,0.32)':`0 0 ${node.priority==='high'?26:16}px ${c.glow}`,display:'flex',alignItems:'center',justifyContent:'center',fontSize:sz*0.34,color:isDone?'#34d399':c.text,position:'relative',zIndex:1}}>
                  {isDone?'✓':isPrq?'◦':node.priority==='high'?'⚡':'→'}
                </div>
                {!isPrq&&<div style={{position:'absolute',bottom:sz+7,left:'50%',transform:'translateX(-50%)',whiteSpace:'nowrap',fontFamily:"'IBM Plex Mono',monospace",fontSize:9,color:isDone?'#34d399':c.text,background:`${c.bg}cc`,border:`1px solid ${c.border}30`,borderRadius:4,padding:'2px 6px'}}>W{node.week_start}–{node.week_end}</div>}
                <div style={{position:'absolute',top:sz+9,left:'50%',transform:'translateX(-50%)',whiteSpace:'nowrap',fontSize:node.priority==='high'?12:11,fontWeight:700,fontFamily:"'DM Sans',sans-serif",color:isDone?'#34d399':isPrq?'#1f2937':c.text,textShadow:isPrq?'none':`0 0 11px ${c.glow}`}}>
                  {node.skill.length>15?node.skill.slice(0,15)+'…':node.skill}
                </div>
                <div style={{position:'absolute',top:sz+24,left:'50%',transform:'translateX(-50%)',whiteSpace:'nowrap',fontSize:9,color:'#252d3d',fontFamily:"'IBM Plex Mono',monospace"}}>{node.duration_weeks}w</div>
              </div>
            )
          })}

          {/* Start — sits on the path line */}
          {(()=>{
            const s = getPathPoint(0)
            const R = 20  // circle radius
            return (
              <div style={{position:'absolute', left: s.x - R, top: s.y - R, zIndex:9}}>
                {/* circle on line */}
                <div style={{width:R*2,height:R*2,borderRadius:'50%',background:'rgba(16,185,129,0.09)',border:'1.5px solid #10b981',display:'flex',alignItems:'center',justifyContent:'center',fontSize:15}}>🚀</div>
                {/* stem up */}
                <div style={{position:'absolute',bottom:'100%',left:'50%',transform:'translateX(-50%)',width:2,height:36,background:'linear-gradient(to bottom,transparent,#10b981)',borderRadius:2}}/>
                {/* label */}
                <div style={{position:'absolute',bottom:'100%',left:'50%',transform:'translateX(-50%)',marginBottom:36,whiteSpace:'nowrap',fontSize:9,fontWeight:700,color:'#10b981',fontFamily:"'IBM Plex Mono',monospace",letterSpacing:1}}>START</div>
              </div>
            )
          })()}

          {/* Goal — sits on the path line */}
          {(()=>{
            const d = getPathPoint(1)
            const R = 26
            return (
              <div style={{position:'absolute', left: d.x - R, top: d.y - R, zIndex:9, animation:'nfloat 3.5s ease-in-out infinite'}}>
                {/* shadow glow under */}
                <div style={{position:'absolute',top:'100%',left:'50%',transform:'translateX(-50%)',marginTop:4,width:40,height:10,background:'rgba(245,158,11,0.15)',borderRadius:'50%',filter:'blur(6px)'}}/>
                {/* circle on line */}
                <div style={{width:R*2,height:R*2,borderRadius:'50%',background:'rgba(245,158,11,0.09)',border:'2px solid #f59e0b',display:'flex',alignItems:'center',justifyContent:'center',boxShadow:'0 0 28px rgba(245,158,11,0.55)',fontSize:20}}>🎯</div>
                {/* stem up */}
                <div style={{position:'absolute',bottom:'100%',left:'50%',transform:'translateX(-50%)',width:2,height:44,background:'linear-gradient(to bottom,transparent,#f59e0b)',borderRadius:2}}/>
                {/* GOAL banner */}
                <div style={{position:'absolute',bottom:'100%',left:'50%',transform:'translateX(-50%)',marginBottom:44,display:'flex',flexDirection:'column',alignItems:'center',gap:4}}>
                  <div style={{whiteSpace:'nowrap',fontSize:11,fontWeight:800,color:'#f59e0b',textShadow:'0 0 14px rgba(245,158,11,0.85)',fontFamily:"'Syne',sans-serif"}}>{target_role}</div>
                  <div style={{background:'linear-gradient(135deg,#f59e0b,#d97706)',borderRadius:6,padding:'3px 14px',boxShadow:'0 0 18px rgba(245,158,11,0.45)'}}>
                    <span style={{fontSize:10,fontWeight:800,color:'#1a0900',letterSpacing:1,fontFamily:"'IBM Plex Mono',monospace"}}>GOAL</span>
                  </div>
                </div>
              </div>
            )
          })()}
        </div>

        {/* Depth fades */}
        <div style={{position:'absolute',top:0,left:0,width:'10%',height:'100%',background:'linear-gradient(to right,#06080f,transparent)',zIndex:10,pointerEvents:'none'}}/>
        <div style={{position:'absolute',top:0,right:0,width:'8%',height:'100%',background:'linear-gradient(to left,#06080f,transparent)',zIndex:10,pointerEvents:'none'}}/>
        <div style={{position:'absolute',top:0,left:0,right:0,height:100,background:'linear-gradient(to bottom,#06080f,transparent)',zIndex:10,pointerEvents:'none'}}/>
        <div style={{position:'absolute',bottom:0,left:0,right:0,height:80,background:'linear-gradient(to top,#06080f,transparent)',zIndex:10,pointerEvents:'none'}}/>

        {/* Hover tooltip */}
        {hovered&&(()=>{
          const links=getResources(hovered.node).slice(0,3)
          const c=PC[hovered.node.priority]
          return (
            <div style={{position:'fixed',zIndex:30,left:Math.min(hovered.x,window.innerWidth-250),top:Math.max(hovered.y-130,80),width:238,background:'rgba(4,5,12,0.97)',border:`1px solid ${c.border}44`,borderRadius:12,padding:'11px 14px',backdropFilter:'blur(20px)',boxShadow:`0 8px 32px ${c.glow.replace('0.4','0.2')}`,pointerEvents:'none',animation:'fadeIn 0.12s ease both'}}>
              <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:8}}>
                <div style={{width:28,height:28,borderRadius:'50%',background:c.bg,border:`1px solid ${c.border}`,display:'flex',alignItems:'center',justifyContent:'center',fontSize:12,color:c.text,flexShrink:0}}>{hovered.node.priority==='high'?'⚡':'→'}</div>
                <div>
                  <div style={{fontFamily:"'Syne',sans-serif",fontSize:13,fontWeight:800,color:'#f8fafc'}}>{hovered.node.skill}</div>
                  <div style={{fontSize:9,color:'#374151',fontFamily:"'IBM Plex Mono',monospace"}}>W{hovered.node.week_start}–{hovered.node.week_end} · {hovered.node.duration_weeks}w</div>
                </div>
              </div>
              {links.length>0?(
                <div style={{display:'flex',flexDirection:'column',gap:4}}>
                  <div style={{fontSize:8,color:'#2d3748',fontFamily:"'IBM Plex Mono',monospace",letterSpacing:'0.06em',marginBottom:2}}>RESOURCES</div>
                  {links.map((lk,i)=>(
                    <div key={i} style={{display:'flex',alignItems:'center',gap:6}}>
                      <span style={{fontSize:10,flexShrink:0}}>{TYPE_ICON[lk.type??'course']??'🔗'}</span>
                      <span style={{fontSize:10,color:lk.free?'#34d399':'#fcd34d',flex:1,overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap'}}>{lk.label}</span>
                      <span style={{fontSize:8,color:lk.free?'#10b981':'#f59e0b',fontFamily:"'IBM Plex Mono',monospace",fontWeight:700,flexShrink:0}}>{lk.free?'FREE':'PAID'}</span>
                    </div>
                  ))}
                  <div style={{fontSize:8,color:'#2d3748',marginTop:2,fontFamily:"'IBM Plex Mono',monospace"}}>click for full details →</div>
                </div>
              ):<div style={{fontSize:10,color:'#374151'}}>click for details & resources</div>}
            </div>
          )
        })()}

        {/* Draggable scrubber */}
        <div style={{position:'absolute',bottom:48,left:'5%',right:'5%',zIndex:15}}>
          <div style={{display:'flex',justifyContent:'space-between',marginBottom:4,padding:'0 2px'}}>
            <span style={{fontSize:9,color:'#1f2937',fontFamily:"'IBM Plex Mono',monospace"}}>START</span>
            <span style={{fontSize:9,color:'#1f2937',fontFamily:"'IBM Plex Mono',monospace"}}>GOAL</span>
          </div>
          <div ref={scrubRef} style={{position:'relative',height:22,cursor:'ew-resize',display:'flex',alignItems:'center'}}>
            <div style={{position:'absolute',left:0,right:0,height:4,background:'rgba(255,255,255,0.05)',borderRadius:2}}>
              <div style={{height:'100%',width:`${scrollPct*100}%`,background:'linear-gradient(90deg,#ef4444,#f59e0b 40%,#8b5cf6)',borderRadius:2,transition:'width 0.05s',boxShadow:'0 0 6px rgba(139,92,246,0.5)'}}/>
              {nodes.map((_,idx)=>{
                const t=nodeT(idx,nodes.length)
                return <div key={idx} style={{position:'absolute',left:`${t*100}%`,top:'50%',transform:'translate(-50%,-50%)',width:5,height:5,borderRadius:'50%',background:PC[nodes[idx].priority].border,boxShadow:`0 0 4px ${PC[nodes[idx].priority].border}`,zIndex:2}}/>
              })}
            </div>
            <div style={{position:'absolute',left:`${scrollPct*100}%`,transform:'translateX(-50%)',width:14,height:14,borderRadius:'50%',background:'#8b5cf6',border:'2px solid rgba(255,255,255,0.2)',boxShadow:'0 0 10px rgba(139,92,246,0.8)',cursor:'grab',zIndex:3,transition:'left 0.05s'}}/>
          </div>
          <div style={{position:'relative',height:20,marginTop:2}}>
            {nodes.filter((_,i)=>i%Math.max(1,Math.floor(nodes.length/7))===0||i===nodes.length-1).map(node=>{
              const idx=nodes.indexOf(node),t=nodeT(idx,nodes.length)
              return (
                <button key={node.id} onClick={()=>goTo(t)} style={{position:'absolute',left:`${t*100}%`,transform:'translateX(-50%)',background:'none',border:'none',color:'#2d3748',fontSize:8,fontFamily:"'IBM Plex Mono',monospace",cursor:'pointer',whiteSpace:'nowrap',padding:'2px 0',transition:'color 0.15s'}}
                  onMouseEnter={e=>(e.currentTarget.style.color='#6b7280')}
                  onMouseLeave={e=>(e.currentTarget.style.color='#2d3748')}
                >{node.skill.length>10?node.skill.slice(0,10)+'…':node.skill}</button>
              )
            })}
          </div>
        </div>

        {/* Click detail panel */}
        {selected&&(()=>{
          const isDone=doneIds.has(selected.id),c=PC[selected.priority],links=getResources(selected)
          return (
            <div style={{position:'absolute',bottom:120,left:'50%',transform:'translateX(-50%)',zIndex:25,width:400,background:'rgba(4,5,12,0.97)',border:`1px solid ${isDone?'rgba(16,185,129,0.3)':c.border+'44'}`,borderRadius:16,backdropFilter:'blur(24px)',boxShadow:`0 8px 50px ${isDone?'rgba(16,185,129,0.12)':c.glow.replace('0.4','0.12')}`,overflow:'hidden',animation:'sUp 0.2s ease both'}}>
              <div style={{padding:'16px 18px 12px',borderBottom:'1px solid rgba(255,255,255,0.04)'}}>
                <div style={{display:'flex',alignItems:'flex-start',gap:11}}>
                  <div style={{width:40,height:40,borderRadius:'50%',flexShrink:0,background:isDone?'rgba(16,185,129,0.1)':c.bg,border:`1.5px solid ${isDone?'#10b981':c.border}`,display:'flex',alignItems:'center',justifyContent:'center',fontSize:16,color:isDone?'#34d399':c.text}}>{isDone?'✓':selected.priority==='high'?'⚡':'→'}</div>
                  <div style={{flex:1}}>
                    <div style={{display:'flex',alignItems:'center',gap:7,flexWrap:'wrap',marginBottom:3}}>
                      <span style={{fontFamily:"'Syne',sans-serif",fontSize:15,fontWeight:800,color:'#f8fafc'}}>{selected.skill}</span>
                      <span style={{fontSize:9,padding:'2px 6px',borderRadius:100,background:isDone?'rgba(16,185,129,0.1)':c.bg,color:isDone?'#34d399':c.text,border:`1px solid ${isDone?'rgba(16,185,129,0.25)':c.border+'44'}`,fontFamily:"'IBM Plex Mono',monospace",textTransform:'uppercase',letterSpacing:0.4}}>{isDone?'done':selected.priority}</span>
                      {selected.is_prerequisite_only&&<span style={{fontSize:9,padding:'2px 6px',borderRadius:100,background:'rgba(255,255,255,0.03)',color:'#374151',border:'1px solid rgba(255,255,255,0.06)',fontFamily:"'IBM Plex Mono',monospace"}}>prereq</span>}
                    </div>
                    <div style={{fontSize:10,color:'#374151',fontFamily:"'IBM Plex Mono',monospace"}}>W{selected.week_start}–{selected.week_end} · {selected.duration_weeks}w · {selected.category}</div>
                  </div>
                  <button onClick={()=>setSelected(null)} style={{background:'none',border:'none',color:'#2d3748',cursor:'pointer',fontSize:15,flexShrink:0}}>✕</button>
                </div>
                <div style={{display:'flex',gap:4,marginTop:11}}>
                  {(['info','links'] as const).map(t2=>(
                    <button key={t2} onClick={()=>setTab(t2)} style={{padding:'4px 12px',borderRadius:5,fontSize:10,fontWeight:600,cursor:'pointer',border:'none',background:tab===t2?(t2==='links'?'#7c3aed':'rgba(255,255,255,0.07)'):'transparent',color:tab===t2?'#f8fafc':'#374151',fontFamily:"'IBM Plex Mono',monospace",transition:'all 0.14s'}}>
                      {t2==='info'?'About':`Study links${links.length?` (${links.length})`:''}`}
                    </button>
                  ))}
                </div>
              </div>
              <div style={{padding:'13px 18px 15px'}}>
                {tab==='info'&&(
                  <>
                    <p style={{fontSize:12,color:'#6b7280',lineHeight:1.65,marginBottom:10}}>{selected.description}</p>
                    {selected.course_title&&(()=>{
                      const firstLink = links.find(l=>l.type==='course') ?? links[0]
                      return (
                        <div style={{background:'rgba(124,58,237,0.05)',border:'1px solid rgba(124,58,237,0.13)',borderRadius:7,padding:'9px 12px',marginBottom:9}}>
                          <div style={{fontSize:8,color:'#374151',fontFamily:"'IBM Plex Mono',monospace",letterSpacing:'0.08em',marginBottom:3}}>RECOMMENDED COURSE</div>
                          {firstLink ? (
                            <a href={firstLink.url} target="_blank" rel="noreferrer" style={{fontSize:12,color:'#a78bfa',textDecoration:'none',display:'block'}}
                              onMouseEnter={e=>(e.currentTarget.style.textDecoration='underline')}
                              onMouseLeave={e=>(e.currentTarget.style.textDecoration='none')}
                            >{selected.course_title} ↗</a>
                          ) : (
                            <div style={{fontSize:12,color:'#a78bfa'}}>{selected.course_title}</div>
                          )}
                          <div style={{fontSize:9,color:'#2d3748',fontFamily:"'IBM Plex Mono',monospace",marginTop:2}}>{selected.course_id?.toUpperCase()}</div>
                        </div>
                      )
                    })()}
                    {selected.prerequisites.length>0&&<div>
                      <div style={{fontSize:8,color:'#2d3748',fontFamily:"'IBM Plex Mono',monospace",letterSpacing:'0.08em',marginBottom:5}}>PREREQUISITES</div>
                      <div style={{display:'flex',flexWrap:'wrap',gap:4}}>{selected.prerequisites.map(p=><span key={p} style={{fontSize:9,background:'rgba(255,255,255,0.03)',border:'1px solid rgba(255,255,255,0.06)',borderRadius:4,padding:'2px 7px',color:'#374151',fontFamily:"'IBM Plex Mono',monospace"}}>{p}</span>)}</div>
                    </div>}
                  </>
                )}
                {tab==='links'&&(
                  <div style={{display:'flex',flexDirection:'column',gap:7}}>
                    {links.length===0?(
                      <div style={{textAlign:'center',padding:'14px 0'}}>
                        <div style={{fontSize:12,color:'#374151',marginBottom:7}}>No curated links yet.</div>
                        <a href={`https://www.google.com/search?q=${encodeURIComponent(selected.skill+' free course tutorial')}`} target="_blank" rel="noreferrer" style={{fontSize:11,color:'#8b5cf6',textDecoration:'none',fontFamily:"'IBM Plex Mono',monospace"}}>Search Google →</a>
                      </div>
                    ):links.map((lk,i)=>(
                      <a key={i} href={lk.url} target="_blank" rel="noreferrer"
                        style={{display:'flex',alignItems:'center',gap:10,background:'rgba(255,255,255,0.02)',border:`1px solid ${lk.free?'rgba(16,185,129,0.13)':'rgba(245,158,11,0.13)'}`,borderRadius:7,padding:'9px 11px',textDecoration:'none',transition:'background 0.13s'}}
                        onMouseEnter={e=>(e.currentTarget.style.background='rgba(255,255,255,0.045)')}
                        onMouseLeave={e=>(e.currentTarget.style.background='rgba(255,255,255,0.02)')}
                      >
                        <div style={{width:28,height:28,borderRadius:6,background:lk.free?'rgba(16,185,129,0.09)':'rgba(245,158,11,0.09)',border:`1px solid ${lk.free?'rgba(16,185,129,0.22)':'rgba(245,158,11,0.22)'}`,display:'flex',alignItems:'center',justifyContent:'center',fontSize:13,flexShrink:0}}>{TYPE_ICON[lk.type??'course']??'🔗'}</div>
                        <div style={{flex:1,minWidth:0}}>
                          <div style={{fontSize:11,color:'#d1d5db',fontWeight:500,overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap'}}>{lk.label}</div>
                          <div style={{fontSize:9,color:'#2d3748',fontFamily:"'IBM Plex Mono',monospace",marginTop:1}}>{lk.url.replace('https://','').split('/')[0]}</div>
                        </div>
                        <span style={{fontSize:9,color:lk.free?'#10b981':'#f59e0b',fontFamily:"'IBM Plex Mono',monospace",fontWeight:700,flexShrink:0}}>{lk.free?'FREE':'PAID'}</span>
                      </a>
                    ))}
                    {links.length>0&&<a href={`https://www.google.com/search?q=${encodeURIComponent(selected.skill+' free course dataset')}`} target="_blank" rel="noreferrer" style={{display:'flex',alignItems:'center',justifyContent:'center',padding:'7px',borderRadius:7,border:'1px dashed rgba(255,255,255,0.05)',color:'#2d3748',fontSize:10,textDecoration:'none',fontFamily:"'IBM Plex Mono',monospace"}}
                      onMouseEnter={e=>(e.currentTarget.style.color='#6b7280')}
                      onMouseLeave={e=>(e.currentTarget.style.color='#2d3748')}
                    >Find more on Google →</a>}
                  </div>
                )}
              </div>
              <div style={{display:'flex',gap:7,padding:'10px 18px 14px',borderTop:'1px solid rgba(255,255,255,0.03)'}}>
                <button onClick={()=>toggleDone(selected.id)} style={{flex:1,background:isDone?'rgba(239,68,68,0.07)':'rgba(16,185,129,0.07)',color:isDone?'#ef4444':'#10b981',border:`1px solid ${isDone?'rgba(239,68,68,0.18)':'rgba(16,185,129,0.18)'}`,padding:'7px 12px',borderRadius:7,fontWeight:600,fontSize:11,cursor:'pointer',fontFamily:"'DM Sans',sans-serif"}}>{isDone?'✗ Mark incomplete':'✓ Mark complete'}</button>
                <button onClick={()=>setSelected(null)} style={{background:'rgba(255,255,255,0.03)',border:'1px solid rgba(255,255,255,0.06)',color:'#4b5563',padding:'7px 12px',borderRadius:7,fontSize:11,cursor:'pointer'}}>Close</button>
              </div>
            </div>
          )
        })()}

        {/* Legend */}
        <div style={{position:'absolute',bottom:14,left:'50%',transform:'translateX(-50%)',zIndex:15,background:'rgba(4,5,12,0.88)',border:'1px solid rgba(255,255,255,0.04)',borderRadius:100,padding:'6px 18px',backdropFilter:'blur(12px)',display:'flex',alignItems:'center',gap:14}}>
          {[['#ef4444','High'],['#f59e0b','Medium'],['#6b7280','Low'],['#10b981','Done']].map(([col,lbl],i)=>(
            <div key={lbl} style={{display:'flex',alignItems:'center',gap:5}}>
              {i>0&&<div style={{width:1,height:10,background:'rgba(255,255,255,0.05)',marginRight:9}}/>}
              <div style={{width:6,height:6,borderRadius:'50%',background:col,boxShadow:`0 0 4px ${col}`}}/>
              <span style={{fontSize:10,color:'#374151',fontFamily:"'DM Sans',sans-serif"}}>{lbl}</span>
            </div>
          ))}
          <div style={{width:1,height:10,background:'rgba(255,255,255,0.05)'}}/>
          <span style={{fontSize:10,color:'#f59e0b',fontWeight:600}}>🎯 {target_role}</span>
        </div>
      </div>

      <style>{`
        @keyframes nfloat{0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)}}
        @keyframes rpulse{0%{transform:scale(1);opacity:.7} 100%{transform:scale(2.3);opacity:0}}
        @keyframes sUp{from{opacity:0;transform:translateX(-50%) translateY(10px)} to{opacity:1;transform:translateX(-50%) translateY(0)}}
        @keyframes fadeIn{from{opacity:0;transform:translateY(4px)} to{opacity:1;transform:translateY(0)}}
        @keyframes spin{to{transform:rotate(360deg)}}
      `}</style>
    </div>
  )
}

function Pill({color,bg,children}:{color:string;bg:string;children:React.ReactNode}){
  return <span style={{background:bg,border:`1px solid ${color}33`,borderRadius:100,padding:'3px 10px',fontSize:10,color,fontFamily:"'IBM Plex Mono',monospace",fontWeight:600}}>{children}</span>
}