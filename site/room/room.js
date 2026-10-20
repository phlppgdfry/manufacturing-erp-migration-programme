// Control room for the fictional Vaerdal Foods ERP programme.
// Everything shown comes from ../data/model.json, which scripts/build.py writes from the same model as the docs.
import { createTour } from "../assets/tour.js";

const GH = "https://github.com/phlppgdfry/manufacturing-erp-migration-programme/blob/main/";
const nf = (d = 0) => new Intl.NumberFormat("nl-BE", { minimumFractionDigits: d, maximumFractionDigits: d });
const num = (v, d = 0) => nf(d).format(v);
const eur = (v, d = 0) => (v < 0 ? "-€" : "€") + nf(d).format(Math.abs(v));
const pct = (v, d = 1) => nf(d).format(v) + "%";
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
const chip = (text, kind = "neutral") => `<span class="chip ${kind}">${esc(text)}</span>`;
const bar = (share, kind = "") => `<div class="bar ${kind}"><span style="width:${Math.max(0, Math.min(100, share))}%"></span></div>`;

let M;
const state = { mock: "mock-3", rule: "DQ-10", gng: "GNG-1", proc: "tobe-order-to-delivery", fgClass: "Alle", fgDomain: "Alle", weights: null, flips: {} };
const view = document.getElementById("view");

// ---------------------------------------------------------------- views

const views = {
  overzicht() {
    const b = M.budget, last = M.mocks.at(-1);
    const maxWeek = 45;
    const rows = M.milestones.map((m) => {
      const plan = m.plannedWeek ? `<span class="tl-mark plan" style="left:${(m.plannedWeek / maxWeek) * 100}%" title="plan W${m.plannedWeek}"></span>` : "";
      const late = m.slip > 0 || m.plannedWeek == null;
      const act = `<span class="tl-mark actual ${late ? "late" : ""}" style="left:${(m.actualWeek / maxWeek) * 100}%" title="werkelijk W${m.actualWeek}"></span>`;
      const slip = m.slip ? `+${m.slip} w` : m.plannedWeek == null ? "nieuw" : "op tijd";
      return `<div class="tl-row"><span>${esc(m.name)}</span><div class="tl-track">${plan}${act}</div><span class="muted">${slip}</span></div>`;
    }).join("");
    const top = M.raidSummary.top.map((r) => `<tr><td>${r.id}</td><td>${esc(r.title)}</td><td class="num">${r.score}</td><td>${esc(r.owner)}</td></tr>`).join("");
    return `
      <h1>Van SAP naar Business Central</h1>
      <p class="intro">${esc(M.org.name)} — ${esc(M.org.products)}. ${num(M.org.employees)} medewerkers, ${num(M.org.erpUsers)} ERP-gebruikers.<br><b>Mijn rol:</b> ${esc(M.role.title)}. ${esc(M.role.summary)}</p>
      <div class="grid cards-4 block" id="tiles">
        <div class="card"><p class="label">Go-live</p><div class="kpi-value">${esc(M.goLiveDates.actual.split(" (")[0])}</div><p class="kpi-sub">gepland ${esc(M.goLiveDates.planned)}</p></div>
        <div class="card"><p class="label">Eindprognose budget</p><div class="kpi-value">${eur(b.eac)}</div><p class="kpi-sub">van ${eur(b.total)} · reserve over ${eur(b.contingencyLeft)}</p></div>
        <div class="card"><p class="label">Standaard of configuratie</p><div class="kpi-value">${M.fitGap.stdConfPct}%</div><p class="kpi-sub">${M.fitGap.extensions} extensies van ${M.fitGap.inScope} eisen in scope</p></div>
        <div class="card"><p class="label">Mock recall (laatste)</p><div class="kpi-value">${pct(last.recall.pct)}</div><p class="kpi-sub">${num(last.recall.found)} van ${num(last.recall.derived)} lots</p></div>
      </div>
      <section class="block card" id="milestones"><h2>Mijlpalen: plan <span class="chip neutral">○</span> en werkelijk <span class="chip ok">●</span></h2><div class="timeline">${rows}</div><p class="note">Schaal: week 1 tot 45. De go-live schoof vier weken op na go/no-go 1.</p></section>
      <section class="block"><h2>Grootste open risico's</h2><div class="table-wrap"><table><thead><tr><th>ID</th><th>Risico</th><th class="num">Score</th><th>Eigenaar</th></tr></thead><tbody>${top}</tbody></table></div></section>`;
  },

  partners() {
    const crit = M.partners.criteria;
    state.weights ??= Object.fromEntries(crit.map((c) => [c.id, c.weight]));
    const total = Object.values(state.weights).reduce((a, b) => a + b, 0) || 1;
    const scores = M.partners.candidates.map((p) => ({ ...p, score: crit.reduce((s, c) => s + p.scores[c.id] * state.weights[c.id], 0) / total }));
    const best = scores.reduce((a, b) => (b.score > a.score ? b : a));
    const sliders = crit.map((c) => `
      <div class="slider-row"><label for="w-${c.id}">${c.id} ${esc(c.name)}</label>
      <input id="w-${c.id}" type="range" min="0" max="100" step="1" value="${state.weights[c.id]}" data-crit="${c.id}">
      <span class="num">${Math.round((state.weights[c.id] / total) * 100)}%</span></div>`).join("");
    const cards = scores.map((p) => `
      <div class="card ${p.id === best.id ? "winner" : ""}">
        <p class="label">${esc(p.name)} ${p.id === best.id ? chip("eerste", "ok") : ""} ${p.id === M.partners.chosen ? chip("gekozen") : ""}</p>
        <div class="kpi-value">${num(p.score, 2)}</div>${bar((p.score / 5) * 100)}
        <p class="kpi-sub">${esc(p.profile)}<br>implementatie ${eur(p.offerImplementation)} · 3 jaar ${eur(p.tco3y)}</p>
      </div>`).join("");
    const sens = M.partners.sensitivity.filter((s) => s.otherWinners.length).map((s) => `<li>${s.id} ${esc(s.name)}: Partner A blijft eerste tot <b>${s.to}%</b> gewicht, daarna ${s.otherWinners.map((w) => w.replace("P-", "Partner ")).join(", ")}</li>`).join("");
    return `
      <h1>Partnerkeuze</h1>
      <p class="intro">De stuurgroep legde criteria en gewichten vast vóór er één offerte binnen was. Schuif zelf met de gewichten: wanneer wint een andere partner?</p>
      <div class="grid cards-3 block" id="partner-scores">${cards}</div>
      <section class="card block" id="weights"><h2>Gewichten</h2>${sliders}<p><button class="btn small" type="button" id="reset-weights">Terug naar de gewichten van de stuurgroep</button></p></section>
      <section class="block"><h2>Gevoeligheid (berekend over 0–100% per criterium)</h2><ul>${sens}</ul><p class="muted">C2, C3, C4 en C7 veranderen de keuze bij geen enkel gewicht. <a href="${GH}docs/02-partnerselectie/README.md">Partnerselectie</a> · <a href="${GH}docs/02-partnerselectie/demoscript.md">demoscript</a> · <a href="${GH}docs/adr/adr-006-contractvorm.md">contractvorm</a></p></section>`;
  },

  processen() {
    const p = M.processes.find((x) => x.id === state.proc);
    const tabs = M.processes.map((x) => `<button type="button" data-proc="${x.id}" aria-pressed="${x.id === state.proc}">${esc(x.name.split(":")[0])}: ${esc(x.name.split(": ")[1])}</button>`).join("");
    const notes = p.notes.map(([k, t]) => `<li><b>${esc(k)}</b> — ${esc(t)}</li>`).join("");
    return `
      <h1>Processen</h1>
      <p class="intro">Zes workshops, telkens vertrekkend van een echt document van vorige week. Rode nummers zijn pijnpunten van vandaag, blauwe letters wat verandert. BPMN 2.0, gegenereerd uit één definitie.</p>
      <div class="tabs" role="group" aria-label="Proces">${tabs}</div>
      <section class="card block" id="process-notes"><h2>${p.kind === "asis" ? "Pijnpunten" : "Wat verandert"}</h2><ul>${notes}</ul></section>
      <figure class="diagram block" id="process-diagram"><img src="../assets/bpmn/${p.id}.svg" alt="${esc(p.name)}"><figcaption>${esc(p.name)} · scroll horizontaal · <a href="${GH}docs/03-processen/bpmn/${p.id}.bpmn">.bpmn-bestand</a></figcaption></figure>`;
  },

  fitgap() {
    const fg = M.fitGap;
    const classes = ["Alle", ...Object.keys(fg.byClass)];
    const domains = ["Alle", ...Object.keys(fg.domains)];
    const rows = M.requirements.filter((r) => (state.fgClass === "Alle" || r.class === state.fgClass) && (state.fgDomain === "Alle" || r.domain === state.fgDomain));
    const kind = { Standaard: "ok", Configuratie: "ok", "ISV-app": "neutral", Procesaanpassing: "warn", Extensie: "risk", "Buiten scope": "neutral" };
    const summary = Object.entries(fg.byClass).map(([k, v]) => `<div class="hbar"><span>${esc(k)}</span>${bar((v / fg.total) * 100, kind[k] === "neutral" ? "" : kind[k])}<span class="num">${v}</span></div>`).join("");
    return `
      <h1>Fit-gap</h1>
      <p class="intro">${fg.total} eisen uit de workshops, elk met een klasse, een oplossing, de bouwdagen van de partner, een beslisser bij Vaerdal en het UAT-scenario dat het bewijst. ${fg.stdConfPct}% van wat in scope is, is standaard of configuratie.</p>
      <section class="card block" id="fg-summary"><h2>Per klasse</h2><div class="hbars">${summary}</div><p class="note">Extensies gaan altijd naar de stuurgroep (ADR-001). Het grafische planbord (CR-03) werd afgewezen.</p></section>
      <div class="tabs" role="group" aria-label="Klasse">${classes.map((c) => `<button type="button" data-fgclass="${esc(c)}" aria-pressed="${c === state.fgClass}">${esc(c)}</button>`).join("")}</div>
      <p><label>Domein <select id="fg-domain">${domains.map((d) => `<option ${d === state.fgDomain ? "selected" : ""}>${esc(d)}</option>`).join("")}</select></label> · ${rows.length} eisen</p>
      <div class="table-wrap" id="fg-table"><table><thead><tr><th>ID</th><th>Eis</th><th>Klasse</th><th>Oplossing</th><th class="num">Dagen</th><th>Beslist door</th><th>Test</th></tr></thead><tbody>
      ${rows.map((r) => `<tr><td>${r.id}</td><td>${esc(r.text)} <span class="muted">(${r.moscow})</span></td><td>${chip(r.class, kind[r.class])}</td><td>${esc(r.solution)}</td><td class="num">${num(r.days, r.days % 1 ? 1 : 0)}</td><td>${esc(r.owner)}</td><td>${r.tests.join(", ") || "—"}</td></tr>`).join("")}
      </tbody></table></div>`;
  },

  migratie() {
    const mk = M.mocks.find((m) => m.id === state.mock);
    const rec = mk.reconciliation;
    const sevKind = { blokkerend: "risk", waarschuwing: "warn", info: "neutral" };
    const tabs = M.mocks.map((m) => `<button type="button" data-mock="${m.id}" aria-pressed="${m.id === state.mock}">${esc(m.name.replace(" (generale repetitie)", " · generale repetitie"))} · W${m.week}</button>`).join("");
    const rows = mk.rules.map((r) => `
      <tr class="clickable ${r.id === state.rule ? "selected" : ""}" data-rule="${r.id}" tabindex="0">
        <td>${r.id}</td><td>${esc(r.title)}<br><span class="muted">${esc(r.object)} · ${esc(r.owner)}</span></td><td>${chip(r.severity, sevKind[r.severity])}</td>
        <td class="num"><b>${num(r.count)}</b></td><td class="num">${r.new == null ? "—" : `${num(r.new)} / ${num(r.carried)}`}</td></tr>`).join("");
    const rule = mk.rules.find((r) => r.id === state.rule) || mk.rules[0];
    const breakdown = rule.breakdown ? `<p><b>Verdeling:</b> ${Object.entries(rule.breakdown).map(([k, v]) => `${esc(k)}: ${num(v)}`).join(" · ")}</p>` : "";
    const newNote = rule.new != null && rule.count ? `<p><b>${num(rule.new)} van ${num(rule.count)} nieuw</b> ten opzichte van de vorige proefmigratie${rule.id === "DQ-10" && rule.new === rule.count && state.mock === "mock-3" ? " — zelfde soort fout, andere lots: de bron maakt nog steeds foute lots." : "."}</p>` : "";
    const detail = `
      <div class="detail" id="rule-detail" style="margin-top:0"><h3>${rule.id} · ${esc(rule.title)}</h3><p class="muted">${esc(rule.why)}</p>${breakdown}${newNote}
      ${rule.sample.length ? `<p><b>Voorbeelden uit het extract</b></p><ul>${rule.sample.map((s) => `<li><code>${esc(s.key)}</code> ${esc(s.detail)}</li>`).join("")}</ul>` : "<p>Geen records gemeld.</p>"}</div>`;
    const day = (iso) => (iso ? iso.slice(8, 10) + "/" + iso.slice(5, 7) : "—");
    const missing = (n) => (n.status === "ontbreekt in BC" ? 1 : 0) + (n.children ?? []).reduce((a, c) => a + missing(c), 0);
    const tree = (n, depth = 0) => {
      const kids = [...(n.children ?? [])].sort((a, b) => missing(b) - missing(a));
      const shown = kids.slice(0, depth === 0 ? 5 : 2);
      const more = kids.length - shown.length;
      return `<li><span class="lot">${esc(n.lot)}</span> ${esc(n.item)} · vervalt ${day(n.expires)} ${chip(n.status, n.status === "in BC" ? "ok" : n.status === "ontbreekt in BC" ? "risk" : "neutral")}${kids.length ? `<ul class="tree">${shown.map((c) => tree(c, depth + 1)).join("")}${more ? `<li class="muted">+ ${more} andere lots</li>` : ""}</ul>` : ""}</li>`;
    };
    const ex = mk.recall.example;
    return `
      <h1>Datamigratie</h1>
      <p class="intro">Vier proefmigraties op gegenereerde SAP-extracten. ${M.dqRules.length} regels, elk met een eigenaar in de business. Klik een regel voor voorbeelden. Blokkerende fouten gaan niet mee.</p>
      <div class="tabs" role="group" aria-label="Proefmigratie">${tabs}</div>
      <div class="grid cards-4 block" id="mig-tiles">
        <div class="card"><p class="label">Blokkerende fouten</p><div class="kpi-value">${num(mk.blocking)}</div><p class="kpi-sub">${num(mk.warnings)} waarschuwingen</p></div>
        <div class="card"><p class="label">Voorraad SAP → BC</p><div class="kpi-value">${pct(rec.stock.diffPct, 3)}</div><p class="kpi-sub">${eur(rec.stock.diff)} op ${eur(rec.stock.sap)}</p></div>
        <div class="card"><p class="label">Openstaande posten</p><div class="kpi-value">${rec.ar.diff === 0 && rec.ap.diff === 0 ? "sluit" : "sluit niet"}</div><p class="kpi-sub">klanten ${eur(rec.ar.diff, 2)} · leveranciers ${eur(rec.ap.diff, 2)}</p></div>
        <div class="card"><p class="label">Mock recall</p><div class="kpi-value">${pct(mk.recall.pct)}</div><p class="kpi-sub">${num(mk.recall.found)} van ${num(mk.recall.derived)} afgeleide lots</p></div>
      </div>
      <section class="block" id="rules"><h2>Datakwaliteit</h2>${detail}<div class="table-wrap" style="margin-top:12px"><table><thead><tr><th>Regel</th><th>Controle</th><th>Ernst</th><th class="num">Gemeld</th><th class="num">Nieuw / bekend</th></tr></thead><tbody>${rows}</tbody></table></div></section>
      <section class="block card" id="reconciliation"><h2>Afstemming voorraad</h2>
        <div class="hbars">
          <div class="hbar"><span>SAP</span>${bar(100)}<span class="num">${eur(rec.stock.sap)}</span></div>
          <div class="hbar"><span>Business Central</span>${bar((rec.stock.bc / rec.stock.sap) * 100, rec.stock.diffPct > 0.1 ? "risk" : "ok")}<span class="num">${eur(rec.stock.bc)}</span></div>
        </div>
        <p class="muted">Verschil verklaard: niet gemigreerde lots ${eur(rec.stock.explained.excludedLots)} · gemiddelde prijs i.p.v. 0 (DQ-14) ${eur(rec.stock.explained.averagePriceFallback)}.</p></section>
      <section class="block card" id="recall"><h2>Mock recall: het slechtst scorende grondstoflot</h2>
        <p class="muted">Leverancierslot ${esc(ex.supplierLot)} → intern lot → afgeleide lots in voorraad. Ontbrekende lots eerst.</p>
        <ul class="tree root">${tree(ex)}</ul></section>`;
  },

  gonogo() {
    const g = M.goNoGo.moments.find((x) => x.id === state.gng);
    const flips = state.flips[g.id] ?? {};
    const crit = g.criteria.map((c) => ({ ...c, pass: flips[c.id] ? !c.pass : c.pass }));
    const decision = decide(crit);
    const tabs = M.goNoGo.moments.map((x) => `<button type="button" data-gng="${x.id}" aria-pressed="${x.id === state.gng}">${x.id} · W${x.week} · voor ${esc(x.forGoLive)}</button>`).join("");
    const rows = crit.map((c) => `<tr><td>${c.id}</td><td>${esc(c.name)}</td><td>${chip(c.type === "hard" ? "hard" : "zacht", c.type === "hard" ? "risk" : "neutral")}</td><td>${esc(c.threshold)}</td><td>${esc(c.value)}${flips[c.id] ? " " + chip("gesimuleerd", "warn") : ""}</td><td>${c.pass ? chip("✓", "ok") : chip("✗", "risk")}</td>
      <td><label class="switch"><input type="checkbox" data-flip="${c.id}" ${flips[c.id] ? "checked" : ""}> omdraaien</label></td></tr>`).join("");
    const simulated = Object.values(flips).some(Boolean);
    const cod = M.costOfDelay.items.map((i) => `<tr><td>${esc(i.line)}</td><td class="num">${eur(i.amount)}</td></tr>`).join("");
    const memo = g.id === "GNG-1" ? `
      <section class="block card" id="memo"><h2>Mijn voorstel aan de stuurgroep</h2>
        <p>G1, G2 en G3 hebben één oorzaak: lots halffabricaat zonder vervaldatum. Ze laden niet, dus ontbreken ze in de voorraad, in de recall en als blokkerende fout.</p>
        <div class="table-wrap"><table><thead><tr><th>Optie</th><th>Kost</th><th>Waarom wel / niet</th></tr></thead><tbody>
          <tr><td>A. Toch live, lots na de go-live met de hand invoeren</td><td>—</td><td>een week niet traceerbaar, audit in mei, een hard criterium achteraf versoepeld ✗</td></tr>
          <tr><td>B. Live zonder halffabricaten, die eerst opgebruiken in SAP</td><td>—</td><td>twee systemen voor voorraad en productie (ADR-002) ✗</td></tr>
          <tr><td><b>C. Vier weken uitstel, eerst de bron herstellen</b></td><td><b>${eur(M.budget.delay)}</b></td><td>hypercare valt in de start van het BBQ-seizoen; maatregelen voorzien ✓</td></tr>
          <tr><td>D. Uitstel tot september</td><td>±€190.000</td><td>vijf maanden langer SAP, partnerteam valt uiteen ✗</td></tr>
        </tbody></table></div>
        <h3>Kost van optie C</h3><div class="table-wrap"><table><tbody>${cod}<tr><td><b>Totaal, uit de reserve</b></td><td class="num"><b>${eur(M.budget.delay)}</b></td></tr></tbody></table></div>
        <p class="muted">Besluit stuurgroep: optie C. Reserve daarna nog ${eur(M.budget.contingencyLeft)}. <a href="${GH}docs/08-go-live/go-no-go.md">Het volledige voorstel</a></p></section>` : `
      <section class="block card" id="memo"><h2>Wat er veranderde in vier weken</h2>
        <ul><li>De SAP-transactie voor halffabricaten werd aangepast; QA herberekende de vervaldatum van bestaande lots.</li><li>Proefmigratie 4: nul blokkerende fouten, recall 100%.</li><li>Defects DEF-07 en DEF-11 opgelost; zeven van zeven EDI-partners getest; 61 van 64 eindgebruikers opgeleid.</li></ul></section>`;
    return `
      <h1>Go/no-go</h1>
      <p class="intro">${esc(M.goNoGo.principle)} ${esc(M.goNoGo.softRule)}</p>
      <div class="tabs" role="group" aria-label="Go/no-go-moment">${tabs}</div>
      <div class="banner ${decision.decision === "GO" ? "go" : "nogo"} block" id="decision">${decision.decision}${simulated ? " (gesimuleerd)" : ""}
        <small>harde criteria gefaald: ${decision.hardFail.join(", ") || "geen"} · zachte criteria gefaald: ${decision.softFail.join(", ") || "geen"}</small></div>
      <section class="block" id="criteria"><div class="table-wrap"><table><thead><tr><th></th><th>Criterium</th><th>Soort</th><th>Drempel</th><th>Gemeten</th><th></th><th>Wat als?</th></tr></thead><tbody>${rows}</tbody></table></div>
      <p class="note">"Omdraaien" simuleert een andere meting, niet een andere regel. ${simulated ? `<button class="btn small" type="button" id="reset-flips">Terug naar de echte metingen</button>` : ""}</p></section>
      ${memo}`;
  },

  budget() {
    const b = M.budget;
    const lines = b.lines.map((l) => `<tr><td>${l.id}</td><td>${esc(l.line)}${l.note ? `<br><span class="muted">${esc(l.note)}</span>` : ""}</td><td class="num">${eur(l.approved)}</td><td class="num">${eur(l.forecast)}</td><td class="num">${eur(l.spent)}</td><td style="min-width:90px">${bar((l.spent / l.forecast) * 100, l.delta > 0 ? "warn" : "")}</td></tr>`).join("");
    const steps = b.steps.map((s) => `<div class="hbar"><span>${esc(s.label)}</span>${bar((s.amount / b.contingency) * 100, "warn")}<span class="num">${eur(s.amount)}</span></div>`).join("");
    const crs = M.changeRequests.map((c) => `<tr><td>${c.id}</td><td>${esc(c.title)}</td><td class="num">${eur(c.cost)}</td><td>${chip(c.decision, c.decision === "goedgekeurd" ? "ok" : "neutral")}</td><td>${esc(c.by)}</td><td class="muted">${esc(c.reason)}</td></tr>`).join("");
    const risks = M.raid.filter((r) => r.type === "Risico");
    let heat = `<div class="axis"></div>${[1, 2, 3, 4, 5].map((i) => `<div class="axis">impact ${i}</div>`).join("")}`;
    for (let p = 5; p >= 1; p--) {
      heat += `<div class="axis">${p}</div>`;
      for (let i = 1; i <= 5; i++) {
        const s = p * i, color = s >= 15 ? "var(--risk-soft)" : s >= 8 ? "var(--warn-soft)" : "var(--ok-soft)";
        heat += `<div class="cell" style="background:${color}">${risks.filter((r) => r.prob === p && r.impact === i).map((r) => `<b title="${esc(r.title)} (${esc(r.status)})">${r.id}</b>`).join("")}</div>`;
      }
    }
    return `
      <h1>Budget &amp; RAID</h1>
      <p class="intro">Programmabudget met 15% reserve. Uitgaven uit de reserve boven ${eur(b.threshold)} beslist de stuurgroep. Interne loonkost zit er niet in.</p>
      <div class="grid cards-4 block" id="budget-tiles">
        <div class="card"><p class="label">Toegekend</p><div class="kpi-value">${eur(b.total)}</div><p class="kpi-sub">${eur(b.subtotal)} + ${eur(b.contingency)} reserve</p></div>
        <div class="card"><p class="label">Reserve gebruikt</p><div class="kpi-value">${eur(b.contingencyUsed)}</div><p class="kpi-sub">over: ${eur(b.contingencyLeft)}</p></div>
        <div class="card"><p class="label">Eindprognose</p><div class="kpi-value">${eur(b.eac)}</div><p class="kpi-sub">binnen het toegekende budget</p></div>
        <div class="card"><p class="label">Afgewezen CR's</p><div class="kpi-value">${eur(b.crRejected)}</div><p class="kpi-sub">zonder die afwijzingen was de reserve op</p></div>
      </div>
      <section class="block card" id="contingency"><h2>Waar de reserve naartoe ging</h2><div class="hbars">${steps}</div></section>
      <section class="block"><h2>Budgetlijnen (stand W18)</h2><div class="table-wrap"><table><thead><tr><th></th><th>Lijn</th><th class="num">Toegekend</th><th class="num">Prognose</th><th class="num">Gefactureerd</th><th></th></tr></thead><tbody>${lines}</tbody></table></div></section>
      <section class="block"><h2>Change requests</h2><div class="table-wrap"><table><thead><tr><th></th><th>Wijziging</th><th class="num">Kost</th><th>Besluit</th><th>Door</th><th>Reden</th></tr></thead><tbody>${crs}</tbody></table></div></section>
      <section class="block card" id="raid"><h2>Risico's: kans × impact</h2><div class="heat">${heat}</div><p class="note">Hover een ID voor de omschrijving. <a href="${GH}docs/governance/raid.md">Volledige RAID-log</a></p></section>`;
  },

  nagolive() {
    const cats = [["data", "Data", "var(--accent)"], ["setup", "Inrichting", "#6b8f71"], ["training", "Opleiding", "var(--warn)"], ["bug", "Bug", "var(--risk)"], ["integration", "Integratie", "#7d7aa6"]];
    const maxWeek = Math.max(...M.hypercare.perWeek);
    const weeks = M.hypercare.tickets.map((w, i) => `<div class="hbar"><span>Week ${w.week}</span><div class="stack" style="width:${(M.hypercare.perWeek[i] / maxWeek) * 100}%">${cats.map(([k, , c]) => `<span style="flex:${w[k]};background:${c}" title="${k}: ${w[k]}"></span>`).join("")}</div><span class="num">${M.hypercare.perWeek[i]}</span></div>`).join("");
    const legend = cats.map(([k, label, c]) => `<span><i style="background:${c}"></i>${label} ${M.hypercare.totals[k]}</span>`).join("");
    const kpis = M.kpis.map((k) => `<tr><td>${esc(k.name)} <span class="muted">(${esc(k.unit)})</span></td><td class="num">${num(k.baseline, k.baseline % 1 ? 1 : 0)}</td><td class="num">${num(k.target, k.target % 1 ? 1 : 0)}</td><td class="num"><b>${num(k.measured, k.measured % 1 ? 1 : 0)}</b></td><td style="min-width:90px">${bar(Math.min(100, k.progress), k.met ? "ok" : "warn")}</td><td>${k.met ? chip("gehaald", "ok") : chip("nog niet", "warn")}</td><td>${esc(k.owner)}</td></tr>`).join("");
    const road = M.roadmap.map((r) => `<tr><td>${esc(r.quarter)}</td><td>${esc(r.item)}</td><td class="muted">${esc(r.why)}</td></tr>`).join("");
    return `
      <h1>Na de go-live</h1>
      <p class="intro">Zes weken hypercare, een batenreview na drie maanden en een roadmap met de IT Manager. ${chip("gesimuleerde resultaten", "warn")}</p>
      <section class="block card" id="hypercare"><h2>Hypercare: ${num(M.hypercare.total)} tickets, ${M.hypercare.bugShare}% bugs</h2><div class="hbars">${weeks}</div><div class="legend">${legend}</div>
        <p class="note">Elk ticket krijgt een oorzaak. De grootste groep is opleiding: een signaal voor de taakkaarten, niet voor de software.</p></section>
      <section class="block" id="kpis"><h2>Batenreview (+3 maanden)</h2><div class="table-wrap"><table><thead><tr><th>KPI</th><th class="num">Vóór</th><th class="num">Doel</th><th class="num">Gemeten</th><th>Voortgang</th><th></th><th>Eigenaar</th></tr></thead><tbody>${kpis}</tbody></table></div>
        <p class="note">Eén van zes doelen gehaald, vijf op weg; elk met een actie. <a href="${GH}docs/09-baten/README.md">Batenreview</a></p></section>
      <section class="block" id="roadmap"><h2>IT-roadmap</h2><div class="table-wrap"><table><tbody>${road}</tbody></table></div></section>
      <section class="block card" id="limits"><h2>Wat deze case niet is</h2><ul>
        <li>Er draait niets in een echte Business Central-omgeving; de migratie zet extracten om, stemt af en traceert, maar laadt niets.</li>
        <li>De SAP-data is gegenereerd, met bewust ingebouwde fouten; testen bewijzen dat de regels precies die fouten vinden.</li>
        <li>Partners, budget, defects, hypercare en KPI's zijn illustratief. Geen echt contract, geen echte stuurgroep.</li>
        <li>Het configureren van Business Central zelf zit in een <a href="https://github.com/phlppgdfry/business-central-implementation-case">aparte case over de partnerkant</a>.</li></ul>
        <p><a href="https://github.com/phlppgdfry/manufacturing-erp-migration-programme">Alle documenten, code en testen op GitHub</a></p></section>`;
  },
};

function decide(results) {
  const hardFail = results.filter((r) => r.type === "hard" && !r.pass).map((r) => r.id);
  const softFail = results.filter((r) => r.type === "soft" && !r.pass).map((r) => r.id);
  return { decision: !hardFail.length && softFail.length <= 2 ? "GO" : "NO-GO", hardFail, softFail };
}

// ---------------------------------------------------------------- routing and events

function current() {
  const v = location.hash.slice(1);
  return views[v] ? v : "overzicht";
}

function render() {
  if (!M) return; // navigation before the model has loaded: the first render follows the fetch
  const name = current();
  view.innerHTML = views[name]();
  document.querySelectorAll(".room-nav a").forEach((a) => {
    if (a.dataset.view === name) a.setAttribute("aria-current", "page");
    else a.removeAttribute("aria-current");
  });
}

function go(name, patch = {}) {
  Object.assign(state, patch);
  if (current() !== name) history.replaceState(null, "", `#${name}`);
  render();
}

view.addEventListener("click", (e) => {
  const t = e.target.closest("[data-mock],[data-rule],[data-gng],[data-proc],[data-fgclass],#reset-weights,#reset-flips");
  if (!t) return;
  if (t.dataset.mock) state.mock = t.dataset.mock;
  if (t.dataset.rule) state.rule = t.dataset.rule;
  if (t.dataset.gng) state.gng = t.dataset.gng;
  if (t.dataset.proc) state.proc = t.dataset.proc;
  if (t.dataset.fgclass) state.fgClass = t.dataset.fgclass;
  if (t.id === "reset-weights") state.weights = null;
  if (t.id === "reset-flips") state.flips[state.gng] = {};
  render();
});
view.addEventListener("keydown", (e) => {
  const row = e.target.closest("[data-rule]");
  if (row && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); state.rule = row.dataset.rule; render(); view.querySelector(`[data-rule="${state.rule}"]`)?.focus(); }
});
view.addEventListener("input", (e) => {
  if (e.target.dataset.crit) {
    state.weights[e.target.dataset.crit] = Number(e.target.value);
    const id = e.target.id;
    render();
    document.getElementById(id)?.focus();
  }
});
view.addEventListener("change", (e) => {
  if (e.target.id === "fg-domain") { state.fgDomain = e.target.value; render(); }
  if (e.target.dataset.flip) {
    state.flips[state.gng] = { ...(state.flips[state.gng] ?? {}), [e.target.dataset.flip]: e.target.checked };
    render();
  }
});
window.addEventListener("hashchange", () => { render(); view.focus({ preventScroll: true }); window.scrollTo(0, 0); });

// ---------------------------------------------------------------- tour

function steps() {
  const m3 = M.mocks.find((m) => m.id === "mock-3"), m4 = M.mocks.at(-1);
  const dq10 = m3.rules.find((r) => r.id === "DQ-10");
  const c6 = M.partners.sensitivity.find((s) => s.id === "C6");
  return [
    { before: () => go("overzicht"), focus: "#tiles", text: `Het probleem: een voedingsproducent (${num(M.org.employees)} mensen) moet van SAP ECC af. Ik leid het programma aan de kant van het bedrijf. De go-live schoof van 1 maart naar 1 april; deze rondleiding toont waarom.` },
    { before: () => go("partners", { weights: null }), focus: "#weights", text: `Eerste keuze: de partner. De stuurgroep legde de gewichten vast vóór de offertes. Prijs weegt 15%. Schuif het prijsgewicht: Partner C wint pas boven ${c6.to}%. De keuze is dus stevig.` },
    { before: () => go("fitgap", { fgClass: "Extensie", fgDomain: "Alle" }), focus: "#fg-table", text: `Fit-gap: ${M.fitGap.stdConfPct}% van de eisen is standaard of configuratie. Van 146 SAP-maatwerkobjecten blijven ${M.fitGap.extensions} extensies over, allebei wettelijk of contractueel. Elke extensie gaat naar de stuurgroep.` },
    { before: () => go("processen", { proc: "tobe-order-to-delivery" }), focus: "#process-notes", text: "To-be in Business Central: elk nieuw lot geblokkeerd tot QA het vrijgeeft (D), picken volgens FEFO met controle op de resterende houdbaarheid per retailer (E). Lots en vervaldatums zijn dus de kern." },
    { before: () => go("migratie", { mock: "mock-3", rule: "DQ-10" }), focus: "#rule-detail", text: `Generale repetitie: ${num(dq10.count)} lots zonder vervaldatum, allemaal halffabricaten uit Hal 2, en ${num(dq10.new)} ervan nieuw ten opzichte van de vorige ronde. Opschonen hielp niet: een SAP-transactie maakte elke dag nieuwe foute lots.` },
    { before: () => go("migratie", { mock: "mock-3", rule: "DQ-10" }), focus: "#recall", text: `Gevolg: de mock recall vindt ${pct(m3.recall.pct)} van de afgeleide lots. Rood = fysiek in de hal, maar niet in Business Central. Bij een echte recall is dat een probleem.` },
    { before: () => go("gonogo", { gng: "GNG-1" }), focus: "#decision", text: `Go/no-go 1: drie harde criteria falen op die ene oorzaak. De criteria lagen vast sinds week 16. Mijn voorstel: vier weken uitstel, eerst de bron herstellen, ${eur(M.budget.delay)} uit de reserve. De stuurgroep besliste.` },
    { before: () => go("gonogo", { gng: "GNG-2" }), focus: "#decision", text: `Go/no-go 2, vier weken later: recall ${pct(m4.recall.pct)}, nul blokkerende fouten. GO voor 1 april.` },
    { before: () => go("nagolive"), focus: "#limits", text: "Na de go-live: hypercare per oorzaak, een eerlijke batenreview (1 van 6 doelen gehaald na drie maanden) en een roadmap. Let op: alle data is gegenereerd en de resultaten zijn gesimuleerd; niets draait in een echte Business Central. Alles staat op GitHub." },
  ];
}

// ---------------------------------------------------------------- start

fetch("../data/model.json")
  .then((r) => r.json())
  .then((model) => {
    M = model;
    render();
    const tour = createTour(steps(), { label: "Rondleiding", labels: { step: "Stap", of: "van", back: "Terug", next: "Volgende", finish: "Klaar", close: "Sluiten" } });
    document.getElementById("btn-tour").addEventListener("click", () => tour.start());
    // ?step=5 opens the tour at that step (used for the screenshots and for deep links)
    const step = Number(new URLSearchParams(location.search).get("step"));
    if (step) setTimeout(() => tour.show(step - 1), 0);
  })
  .catch(() => { view.innerHTML = `<p>De gegevens konden niet geladen worden. <a href="https://github.com/phlppgdfry/manufacturing-erp-migration-programme/tree/main/docs/screenshots">Bekijk de screenshots</a>.</p>`; });
