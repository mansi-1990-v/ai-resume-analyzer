import React, { useState } from 'react';
import { Upload, FileText, CheckCircle, AlertTriangle, Briefcase, User, Star, TrendingUp, Search } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import {
    Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer,
    Bar, BarChart, XAxis, YAxis, Tooltip, CartesianGrid
} from 'recharts';

export default function App() {
    const [file, setFile] = useState(null);
    const [jobDescription, setJobDescription] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [activeTab, setActiveTab] = useState('overview'); // overview, xray, xai

    const handleFileUpload = (e) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const submitAnalysis = async () => {
        if (!file || !jobDescription) return alert('Please provide both resume and job description.');
        setIsLoading(true);

        try {
            // 1. Upload Resume
            const formData = new FormData();
            formData.append('file', file);

            const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
            const uploadRes = await axios.post(`${apiUrl}/analyze/resume`, formData);
            const resumeData = uploadRes.data.resume_data;
            const rawText = resumeData.raw_text;

            // 2. Job Fit
            const jobFitForm = new FormData();
            jobFitForm.append('resume_text', rawText);
            jobFitForm.append('job_description', jobDescription);

            const fitRes = await axios.post(`${apiUrl}/analyze/job-fit`, jobFitForm);
            const fitData = fitRes.data;

            setResult({
                overall_score: fitData.overall_score,
                breakdown: {
                    skills: fitData.breakdown.skills_match,
                    experience: fitData.breakdown.experience_match,
                    ats: uploadRes.data.quality_evaluation.overall_score
                },
                skills_matched: fitData.matching_skills,
                skills_missing: fitData.missing_skills,
                xai_explanation: fitData.explanation,
                predicted_roles: uploadRes.data.predicted_roles,
                ats_suggestions: uploadRes.data.quality_evaluation.suggestions
            });
        } catch (error) {
            alert("Error analyzing resume. Make sure backend is running: " + error.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-background relative overflow-hidden">
            {/* Abstract Background Gradients */}
            <div className="absolute top-0 -left-[20%] w-[50%] h-[50%] bg-primary/20 blur-[120px] rounded-full point-events-none" />
            <div className="absolute bottom-0 -right-[20%] w-[50%] h-[50%] bg-secondary/20 blur-[120px] rounded-full point-events-none" />

            <div className="max-w-7xl mx-auto px-6 py-12 relative z-10">

                {/* Header */}
                <header className="flex justify-between items-center mb-12 animate-fade-in border-b border-white/5 pb-4">
                    <div className="flex items-center gap-3">
                        <div className="h-8 w-8 bg-white flex items-center justify-center">
                            <span className="text-black font-black text-xl leading-none tracking-tighter">H</span>
                        </div>
                        <h1 className="text-xl font-black text-white tracking-widest uppercase flex items-center gap-2">
                            HireSense <span className="text-primary font-mono text-xs px-2 py-0.5 bg-primary/10 rounded-full border border-primary/20">v2.0</span>
                        </h1>
                    </div>
                    <a href="https://github.com/abhishekkumar/ai-resume-analyzer" target="_blank" className="btn-secondary py-1.5 px-3 text-xs font-mono hidden md:flex">
                        [SOURCE_CODE]
                    </a>
                </header>

                {!result ? (
                    /* ELITE MINIMALIST INPUT HERO STAGE */
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex flex-col items-center justify-center min-h-[70vh] w-full max-w-4xl mx-auto px-4 mt-8">

                        <div className="text-center mb-16 animate-fade-in">
                            <h2 className="text-5xl md:text-6xl font-black tracking-tighter text-white mb-6 leading-tight">
                                Deep Semantic <br /> <span className="text-transparent bg-clip-text bg-gradient-to-r from-zinc-400 to-zinc-600">Resume Analysis.</span>
                            </h2>
                            <p className="text-secondary text-lg font-medium tracking-wide max-w-2xl mx-auto">
                                Drop a resume. Provide a JD. Our RAG-enhanced vector engine will calculate explicit and implicit ontological match scores in seconds.
                            </p>
                        </div>

                        {/* Interactive IDE-Style Workspace */}
                        <div className="w-full relative group pb-12">

                            {/* Hover Core Bleed */}
                            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full h-full bg-primary/5 blur-[100px] rounded-full pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-1000 z-0" />

                            <div className="relative z-10 w-full surface-panel rounded-3xl p-2 shadow-2xl overflow-hidden flex flex-col md:flex-row gap-2">

                                {/* 1. Massive Drop Zone (Left/Top) */}
                                <div className="relative flex-1 bg-black rounded-2xl border border-borderclr/50 hover:border-primary/30 transition-colors duration-500 overflow-hidden cursor-pointer h-72 flex flex-col items-center justify-center p-8 text-center group/drop">
                                    <input type="file" className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-20" onChange={handleFileUpload} accept=".pdf,.docx,.txt" />

                                    {/* Abstract Grid Background */}
                                    <div className="absolute inset-0 opacity-[0.03] group-hover/drop:opacity-[0.08] transition-opacity duration-500" style={{ backgroundImage: 'linear-gradient(to right, #fff 1px, transparent 1px), linear-gradient(to bottom, #fff 1px, transparent 1px)', backgroundSize: '24px 24px' }} />

                                    <motion.div
                                        animate={{ y: file ? 0 : [0, -5, 0] }}
                                        transition={{ repeat: file ? 0 : Infinity, duration: 4, ease: "easeInOut" }}
                                        className="h-16 w-16 bg-surface rounded-xl border border-borderclr flex items-center justify-center mb-6 shadow-xl relative z-10 group-hover/drop:border-primary/50 transition-colors"
                                    >
                                        <Upload className={`w-8 h-8 ${file ? 'text-primary' : 'text-secondary'}`} strokeWidth={1.5} />
                                    </motion.div>

                                    <div className="relative z-10">
                                        <h3 className="text-white font-bold text-xl mb-2 tracking-tight">
                                            {file ? file.name : "Initialize Document"}
                                        </h3>
                                        <p className="text-secondary text-sm font-medium">
                                            {file ? "File buffered for extraction." : "Drag & drop PDF, DOCX, or TXT."}
                                        </p>
                                    </div>
                                </div>

                                {/* 2. Command Palette Job Description (Right/Bottom) */}
                                <div className="flex-1 bg-surface rounded-2xl flex flex-col relative h-72">
                                    <div className="px-6 py-4 border-b border-borderclr/50 flex items-center justify-between">
                                        <div className="flex items-center gap-2">
                                            <div className="w-2 h-2 rounded-full bg-accent animate-pulse-glow" />
                                            <span className="label-mono">Target Protocol [JD]</span>
                                        </div>
                                    </div>
                                    <div className="flex-1 relative p-2">
                                        <textarea
                                            className="w-full h-full bg-black/50 border border-transparent hover:border-borderclr/50 rounded-xl p-5 text-sm font-mono text-zinc-300 focus:outline-none focus:border-primary/50 focus:bg-black resize-none transition-all placeholder:text-zinc-700 custom-scrollbar leading-relaxed"
                                            placeholder="> PASTE TARGET REQUIREMENTS HERE...&#10;> WAITING FOR INPUT..."
                                            value={jobDescription}
                                            onChange={(e) => setJobDescription(e.target.value)}
                                            spellCheck={false}
                                        />
                                    </div>
                                </div>

                            </div>

                            {/* Center Submit Action */}
                            <div className="absolute left-1/2 -bottom-6 -translate-x-1/2 z-20">
                                <button
                                    onClick={submitAnalysis}
                                    disabled={isLoading}
                                    className={`relative group ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
                                >
                                    <div className="absolute -inset-1 bg-white rounded-full blur opacity-20 group-hover:opacity-40 transition duration-500"></div>
                                    <div className="relative btn-primary rounded-full pl-8 pr-6 py-4 shadow-2xl border border-white/20">
                                        {isLoading ? (
                                            <span className="flex items-center gap-3">
                                                <div className="w-4 h-4 border-2 border-black/30 border-t-black rounded-full animate-spin" />
                                                <span className="font-bold tracking-widest text-xs uppercase">Computing...</span>
                                            </span>
                                        ) : (
                                            <span className="flex items-center gap-3">
                                                <span className="font-bold tracking-widest text-xs uppercase">Execute Analysis</span>
                                                <TrendingUp className="w-4 h-4 translate-x-0 group-hover:translate-x-1 transition-transform" />
                                            </span>
                                        )}
                                    </div>
                                </button>
                            </div>
                        </div>
                    </motion.div>
                ) : (
                    /* ELITE MINIMALIST RESULTS STAGE */
                    <motion.div initial={{ opacity: 0, scale: 0.98 }} animate={{ opacity: 1, scale: 1 }} className="w-full max-w-6xl mx-auto space-y-4">

                        {/* Header bar */}
                        <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-6 pb-6 border-b border-borderclr/50">
                            <div>
                                <h2 className="text-3xl font-black text-white tracking-tighter mb-1 select-none">Candidate Profiling Complete.</h2>
                                <p className="text-secondary tracking-wide text-sm font-medium">Multidimensional scalar evaluation against `{jobDescription.substring(0, 30)}...`</p>
                            </div>
                            <button onClick={() => setResult(null)} className="btn-secondary group">
                                <Search className="w-4 h-4 group-hover:-scale-x-100 transition-transform" />
                                Run New Query
                            </button>
                        </div>

                        {/* Top Data Row: Metric brutalism */}
                        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">

                            {/* Primary Metric: Massive Typography */}
                            <div className="md:col-span-2 surface-panel p-6 flex flex-col justify-between relative overflow-hidden group">
                                <div className="absolute -bottom-10 -right-10 w-40 h-40 bg-white/5 blur-[50px] group-hover:bg-white/10 transition-colors" />
                                <span className="label-mono flex items-center gap-2">
                                    <div className="w-1.5 h-1.5 bg-primary rounded-full animate-pulse" />
                                    Overall Match Vector
                                </span>

                                <div className="mt-8 flex items-baseline gap-2">
                                    <span className="text-7xl md:text-8xl font-black tracking-tighter text-white leading-none">
                                        {result.overall_score}
                                    </span>
                                    <span className="text-2xl font-bold text-secondary">/100</span>
                                </div>
                            </div>

                            {/* Secondary Metrics */}
                            <div className="surface-panel p-6 flex flex-col justify-between">
                                <span className="label-mono">Semantic Fit</span>
                                <div className="mt-8 relative">
                                    <span className="text-5xl font-black tracking-tighter text-white">{result.breakdown.skills}%</span>
                                    <div className="w-full h-1 bg-borderclr mt-4">
                                        <div className="h-full bg-white transition-all duration-1000" style={{ width: `${result.breakdown.skills}%` }} />
                                    </div>
                                </div>
                            </div>

                            <div className="surface-panel p-6 flex flex-col justify-between">
                                <span className="label-mono">ATS Integrity</span>
                                <div className="mt-8 relative">
                                    <span className="text-5xl font-black tracking-tighter text-white">{result.breakdown.ats}%</span>
                                    <div className="w-full h-1 bg-borderclr mt-4">
                                        <div className="h-full bg-secondary transition-all duration-1000" style={{ width: `${result.breakdown.ats}%` }} />
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Middle Data Row: Analysis & Radar */}
                        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">

                            {/* XAI Text Output */}
                            <div className="lg:col-span-2 surface-panel p-6 flex flex-col relative group overflow-hidden">
                                <div className="absolute top-0 right-0 w-64 h-64 bg-accent/5 blur-[80px] pointer-events-none group-hover:bg-accent/10 transition-colors" />

                                <div className="flex items-center gap-2 mb-6">
                                    <Star className="w-4 h-4 text-accent" />
                                    <span className="label-mono">XAI Synthesis</span>
                                </div>

                                <div className="mb-8 border-l-2 border-primary pl-4">
                                    <p className="text-lg md:text-xl text-zinc-300 font-medium leading-relaxed tracking-tight">
                                        "{result.xai_explanation}"
                                    </p>
                                </div>

                                <div className="grid grid-cols-2 gap-4 mt-auto">
                                    <div className="p-4 bg-black/40 border border-borderclr/50 rounded-lg">
                                        <span className="label-mono mb-3 block text-zinc-500">Positive Signals</span>
                                        <div className="flex flex-wrap gap-1.5">
                                            {result.skills_matched.map(s => <span key={s} className="px-2 py-1 bg-white/5 text-white text-xs font-mono tracking-wide rounded border border-white/10">{s}</span>)}
                                        </div>
                                    </div>
                                    <div className="p-4 bg-black/40 border border-borderclr/50 rounded-lg">
                                        <span className="label-mono mb-3 block text-zinc-500">Missing Vectors</span>
                                        <div className="flex flex-wrap gap-1.5">
                                            {result.skills_missing.map(s => <span key={s} className="px-2 py-1 bg-error/10 text-error text-xs font-mono tracking-wide rounded border border-error/20">{s}</span>)}
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Dimensional Radar */}
                            <div className="surface-panel p-6 flex flex-col min-h-[400px]">
                                <span className="label-mono mb-6 block">Dimensional Mapping</span>
                                <div className="flex-1 w-full bg-black/30 border border-borderclr/50 rounded-xl relative">
                                    <ResponsiveContainer width="100%" height="100%">
                                        <RadarChart cx="50%" cy="50%" outerRadius="70%" data={[
                                            { subject: 'Backend', A: 90, fullMark: 100 },
                                            { subject: 'Frontend', A: 40, fullMark: 100 },
                                            { subject: 'DevOps', A: 70, fullMark: 100 },
                                            { subject: 'Cloud', A: 85, fullMark: 100 },
                                            { subject: 'Data Base', A: 95, fullMark: 100 },
                                            { subject: 'System', A: 80, fullMark: 100 },
                                        ]}>
                                            <PolarGrid stroke="#27272a" strokeDasharray="3 3" />
                                            <PolarAngleAxis dataKey="subject" tick={{ fill: '#a1a1aa', fontSize: 10, fontFamily: 'JetBrains Mono', textAnchor: 'middle' }} />
                                            <Radar name="Candidate" dataKey="A" stroke="#fafafa" strokeWidth={1} fill="#fafafa" fillOpacity={0.1} />
                                            <Tooltip contentStyle={{ backgroundColor: '#000', borderColor: '#27272a', borderRadius: '4px', fontFamily: 'JetBrains Mono', fontSize: '12px' }} />
                                        </RadarChart>
                                    </ResponsiveContainer>
                                </div>
                            </div>
                        </div>

                        {/* Bottom Row: Terminal Lists */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

                            <div className="surface-panel p-6">
                                <span className="label-mono mb-6 block flex items-center gap-2"><User className="w-3 h-3" /> ML Predicted Roles</span>
                                <div className="space-y-4">
                                    {result.predicted_roles.map((r, i) => (
                                        <div key={i} className="group cursor-default">
                                            <div className="flex justify-between items-center mb-2">
                                                <span className="text-sm font-semibold text-white tracking-wide group-hover:text-primary transition-colors">{r.role}</span>
                                                <span className="font-mono text-xs text-secondary">{r.confidence}% Match</span>
                                            </div>
                                            <div className="w-full bg-borderclr h-[2px] overflow-hidden">
                                                <div className="bg-white h-full" style={{ width: `${r.confidence}%` }}></div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            <div className="surface-panel p-6">
                                <span className="label-mono mb-6 block flex items-center gap-2"><CheckCircle className="w-3 h-3" /> ATS Diagnostics</span>
                                <ul className="space-y-3 custom-scrollbar overflow-y-auto max-h-[160px] pr-2">
                                    {result.ats_suggestions.map((s, i) => (
                                        <li key={i} className="text-sm text-zinc-400 flex items-start gap-3 p-3 bg-black/50 border border-borderclr/50 rounded hover:border-borderclr transition-colors">
                                            <div className="w-1.5 h-1.5 bg-zinc-600 rounded-full mt-1.5 shrink-0" />
                                            <span className="leading-relaxed tracking-wide">{s}</span>
                                        </li>
                                    ))}
                                </ul>
                            </div>

                        </div>

                    </motion.div>
                )}
            </div>
        </div>
    );
}
