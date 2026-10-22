#!/usr/bin/env node
/* Acceptance briefs only. New assignments require new storyboards and source. */
const fs=require('fs'), path=require('path'), PptxGenJS=require('pptxgenjs');
const out=path.resolve(process.argv[2]||'work/acceptance');fs.mkdirSync(out,{recursive:true});
const data=JSON.parse(fs.readFileSync(path.join(__dirname,'../examples/data.json'),'utf8'));
const W=13.333333,H=7.5;
function deck(title,font='DejaVu Sans') {const p=new PptxGenJS();p.layout='LAYOUT_WIDE';p.author='Research & Design Studio';p.subject='Fictional acceptance test, 2026-10-22';p.title=title;p.company='Studio';p.lang='ru-RU';p.theme={headFontFace:font,bodyFontFace:font,lang:'ru-RU'};return p;}
function text(s,t,x,y,w,h,size=22,color='162C35',opt={}){s.addText(t,{x,y,w,h,fontSize:size,color,fontFace:'DejaVu Sans',margin:0,breakLine:false,vertAnchor:'mid',...opt});}
function rect(s,x,y,w,h,color,opt={}){s.addShape('rect',{x,y,w,h,line:{color,transparency:100},fill:{color},...opt});}
function line(s,x,y,w,color='C9D2D2',width=0.8){s.addShape('line',{x,y,w,h:0,line:{color,width}});}
function circle(s,x,y,w,h,color,opt={}){s.addShape('ellipse',{x,y,w,h,line:{color,transparency:100},fill:{color},...opt});}
function note(s,txt){s.addNotes(txt);}
function footer(s,idx,label='ДЕМОНСТРАЦИЯ · УСЛОВНЫЕ ДАННЫЕ',color='5B7078'){text(s,label,0.55,7.05,11.5,.2,8.5,color);text(s,String(idx).padStart(2,'0'),12.15,7.02,.6,.25,10,color,{align:'right'});}
function stHead(s,k,title,sub){text(s,k.toUpperCase(),.55,.38,11,.3,10,'00796D',{charSpacing:1.3,bold:true});text(s,title,.55,.95,12.05,1.05,29,'162C35',{bold:true});if(sub)text(s,sub,.55,2.03,11.8,.45,13,'5B7078');}
function annotation(s,num,title,desc,y){text(s,num,.6,y,.55,.55,22,'00796D',{bold:true});text(s,title,1.4,y,6.5,.45,19,'162C35',{bold:true});text(s,desc,1.4,y+.5,6.7,.6,14,'5B7078');}

async function strategy(){const p=deck('Решение: пилот студии исследований');let s;
 s=p.addSlide();s.background={color:'F7F8F5'};
 rect(s,9.1,0,4.233333,7.5,'163E46');text(s,'RESEARCH\nOPERATIONS',.6,.5,7,.6,12,'00796D',{bold:true,charSpacing:2});
 text(s,'Освободить время\nдля решений',.6,2.03,8.1,1.75,40,'162C35',{bold:true});
 text(s,'12-недельный пилот единого процесса\nисследования, дизайна и проверки',.65,4.2,7.7,.9,20,'5B7078');
 text(s,'−35%',9.55,2.2,3.3,1.25,64,'FFFFFF',{bold:true});text(s,'целевая трудоёмкость\nусловного отчёта',9.6,3.72,3.1,.85,17,'C4DDD6');
 text(s,'РЕШЕНИЕ ДЛЯ РУКОВОДСТВА\n22 октября 2026',.65,6.08,7,.6,11,'5B7078');footer(s,1,'ТЕСТ СТРАТЕГИЧЕСКОЙ ПРЕЗЕНТАЦИИ · МОДЕЛЬ, НЕ ФАКТ');
 note(s,'All values are synthetic. Source: studio/examples/data.json strategy. Reduction=(40−26)/40=35%. This is a proposed target, not an observed result.');
 s=p.addSlide();s.background={color:'F7F8F5'};stHead(s,'Решение за одну минуту','Запустить пилот с проверкой качества','Цель — проверить целевую экономию времени без ухудшения аргументации.');
 annotation(s,'01','Единый путь от вопроса до результата','Источники, структура и визуальная система сохраняются вместе.',2.9);
 annotation(s,'02','Проверка становится отдельным этапом','Факты и каждый слайд проверяются до выдачи результата.',4.2);
 rect(s,9.1,2.75,3.65,3.8,'E4EDE6');text(s,'УСЛОВИЕ ПРОДОЛЖЕНИЯ',9.4,3.1,3.05,.45,11,'00796D',{bold:true});text(s,'0',9.4,3.75,2.8,1.1,66,'163E46',{bold:true});text(s,'неустранённых\nкритических ошибок',9.45,5.1,2.85,.8,17,'163E46');footer(s,2);note(s,'Recommendation for the fictional pilot. Zero blockers is a proposed acceptance criterion, not observed data.');
 s=p.addSlide();s.background={color:'F7F8F5'};stHead(s,'Операционная модель','Цель пилота: 40 → 26 часов на отчёт','Наибольший резерв модели — поиск материалов и сборка слайдов.');
 s.addChart(p.ChartType.bar,[{name:'До',labels:data.strategy.stage_names,values:data.strategy.before_hours},{name:'Цель',labels:data.strategy.stage_names,values:data.strategy.after_hours}],{x:.6,y:2.8,w:8.65,h:3.65,barDir:'col',catAxisLabelFontFace:'DejaVu Sans',catAxisLabelFontSize:12,valAxisLabelFontSize:10,valAxisMinVal:0,valAxisMaxVal:14,valAxisMajorUnit:2,showLegend:true,legendPos:'b',legendFontSize:11,showTitle:false,showValue:true,dataLabelPosition:'outEnd',dataLabelFormatCode:'0',chartColors:['BAC8CC','00796D'],showBorder:false,showCatName:false,showShadow:false,valGridLine:{color:'DAE2E1',width:.5},showCatName:false,showSerName:false,showMarker:false,showCatName:false});
 text(s,'Часы / отчёт',.65,2.48,3,.25,10,'5B7078');text(s,'−14 ч',9.65,3.1,3,1,48,'00796D',{bold:true});text(s,'Расчётная разница\nв условной модели.\n\nЭффект предстоит\nизмерить в пилоте.',9.65,4.35,2.9,1.7,16,'5B7078');footer(s,3,'ИСТОЧНИК: examples/data.json · strategy · ВСЕ ЗНАЧЕНИЯ УСЛОВНЫЕ');note(s,'Native editable chart with embedded workbook. Before 12+10+10+8=40; target 8+7+6+5=26. The target is not empirical evidence.');
 s=p.addSlide();s.background={color:'F7F8F5'};stHead(s,'Выбор подхода','Пилот даёт проверяемое основание для масштаба','Качественная оценка вариантов; финансовая окупаемость пока не рассчитана.');
 const cols=[.65,5.25,8.9],ys=[2.85,3.65,4.55,5.45];
 text(s,'Критерий',cols[0],ys[0],4,.4,12,'5B7078',{bold:true});text(s,'Разрозненные инструменты',cols[1],ys[0],3.2,.55,14,'5B7078',{bold:true});rect(s,8.65,2.65,4.1,3.7,'E4EDE6');text(s,'Единый пилот',cols[2],ys[0],3.4,.4,17,'00796D',{bold:true});
 [['Источники и версии','Зависят от автора','Общий журнал'],['Проверка слайдов','По ситуации','Перед выдачей'],['Решение о масштабе','Без общей метрики','По результатам пилота']].forEach((r,i)=>{const y=ys[i+1];line(s,.65,y-.12,12,'CBD6D4');r.forEach((v,j)=>text(s,v,cols[j],y,j?3.3:4,.65,j?15:16,j===2?'163E46':'304B54'));});footer(s,4);note(s,'Qualitative recommendation and proposed controls; not a measured comparison.');
 s=p.addSlide();s.background={color:'163E46'};text(s,'12 НЕДЕЛЬ',.6,.5,10,.4,12,'BCD7CB',{charSpacing:1.5});text(s,'Измерить. Исправить.\nПринять решение.',.6,1.42,11.8,1.45,37,'FFFFFF',{bold:true});
 [['01–02','База','Руководитель аналитики\nЗамерить время и ошибки'],['03–08','Пилот','Команда студии\nПроверить три типа задач'],['09–12','Решение','Заказчик пилота\nОценить качество и эффект']].forEach((r,i)=>{const x=.7+i*4.18;line(s,x,3.55,3.7,'6B9899');text(s,r[0],x,3.85,3.65,.55,29,'C6E8D1',{bold:true});text(s,r[1],x,4.58,3.7,.4,20,'FFFFFF',{bold:true});text(s,r[2],x,5.25,3.65,.85,15,'C4DDD6');});footer(s,5,'ПРЕДЛОЖЕННЫЙ ПЛАН · СРОКИ И РОЛИ ДЛЯ ДЕМОНСТРАЦИИ','B1CBC6');note(s,'Proposed 12-week plan with role owners. No dates or commitments are real.');
 s=p.addSlide();s.background={color:'F7F8F5'};stHead(s,'Основания и границы','Эта модель проверяет процесс, а не рынок','Ни одна коммерческая цифра не выдается за результат реального исследования.');
 text(s,'Данные',.65,2.8,3,.4,18,'00796D',{bold:true});text(s,'Локальный открытый файл examples/data.json.\nВсе трудозатраты заданы для теста.\nЭкономия: (40 − 26) / 40 = 35%.',.65,3.45,6.05,1.5,17,'304B54');
 text(s,'Что нужно измерить',7.3,2.8,5,.4,18,'00796D',{bold:true});text(s,'Фактическое время команды.\nТяжесть ошибок до и после.\nДолю выводов с достаточным обоснованием.\nОценку читабельности заказчиком.',7.3,3.45,5.25,1.85,17,'304B54');
 line(s,.65,6.1,12);text(s,'Референсы и журнал доступа: studio/references/design-references.json\nАрт-дирекшн и QA поставляются отдельно от презентации.',.65,6.3,11.8,.5,11,'5B7078');footer(s,6);note(s,'Source locator: studio/examples/data.json. Visual-reference access and limitations are logged separately.');
 await p.writeFile({fileName:path.join(out,'01-strategy.pptx')});
}

function pitFoot(s,i){footer(s,i,'TRACE / FICTIONAL PITCH · ВСЕ ПОКАЗАТЕЛИ УСЛОВНЫЕ','92958F');}
async function pitch(){const p=deck('TRACE — fictional investor pitch');let s;
 s=p.addSlide();s.background={color:'111512'};text(s,'TRACE',.55,.45,6,.5,24,'D4F28B',{bold:true,charSpacing:3});
 text(s,'У каждого вывода\nесть след.',.55,1.85,10.9,1.95,52,'F5F7EE',{bold:true});
 text(s,'Рабочее пространство доказательств\nдля исследовательских команд',.62,4.6,8.5,.9,22,'B4BDB0');
 line(s,.65,6.3,11.95,'526047');text(s,'ВЫМЫШЛЕННЫЙ ПРОДУКТ / SEED CONCEPT',.65,6.52,11.5,.3,11,'D4F28B');pitFoot(s,1);note(s,'Fictional company and product, no observed market performance.');
 s=p.addSlide();s.background={color:'D4F28B'};text(s,'ПРОБЛЕМА',.6,.5,10,.35,12,'1D311F',{bold:true,charSpacing:2});
 text(s,'Ссылка потерялась.\nУверенность — тоже.',.6,1.5,11.9,1.8,45,'111512',{bold:true});
 const xx=[.7,4.75,9];['Сохранили URL','Перенесли цифру','Забыли контекст'].forEach((v,i)=>{text(s,String(i+1).padStart(2,'0'),xx[i],4.25,3,.6,31,'3D5E2C',{bold:true});line(s,xx[i],5.08,3.6,'6F8A4E');text(s,v,xx[i],5.4,3.5,.75,18,'1D311F',{bold:true});});footer(s,2,'ГИПОТЕЗА ПРОБЛЕМЫ · ТРЕБУЕТ ИНТЕРВЬЮ С ПОЛЬЗОВАТЕЛЯМИ','3D5E2C');note(s,'Problem hypothesis; not a factual claim about all research teams.');
 s=p.addSlide();s.background={color:'111512'};text(s,'ПРОДУКТ',.6,.5,10,.35,12,'D4F28B',{charSpacing:2});text(s,'От источника\nдо решения.',.6,1.25,5.1,1.7,40,'F5F7EE',{bold:true});
 [['01','Источник','Фрагмент, дата, страница'],['02','Утверждение','Число, единица, период'],['03','Результат','Отчёт, слайд, проверка']].forEach((r,i)=>{const y=1.7+i*1.47;rect(s,6.45,y,6.25,1.1,i===1?'D4F28B':'263225');text(s,r[0],6.7,y+.28,.8,.4,17,i===1?'23331D':'D4F28B',{bold:true});text(s,r[1],7.65,y+.13,4.6,.4,20,i===1?'111512':'F5F7EE',{bold:true});text(s,r[2],7.65,y+.63,4.7,.3,12,i===1?'3D5E2C':'B4BDB0');});text(s,'Концепция интерфейса.\nНе готовый программный продукт.',.65,4.85,5.3,.9,16,'B4BDB0');pitFoot(s,3);note(s,'Original diagram of a hypothetical product workflow, all native editable shapes.');
 s=p.addSlide();s.background={color:'111512'};text(s,'СЦЕНАРИЙ ПИЛОТА',.6,.5,10,.35,12,'D4F28B',{charSpacing:2});text(s,'24 команды.\n18 продолжают.',.6,1.25,7.1,1.45,36,'F5F7EE',{bold:true});text(s,'75%',9.15,1.25,3.55,1.1,62,'D4F28B',{bold:true});text(s,'условное удержание',9.2,2.55,3.45,.45,14,'B4BDB0');
 s.addChart(p.ChartType.line,[{name:'Активные команды',labels:data.pitch.months,values:data.pitch.active_teams}],{x:.55,y:3.45,w:12.1,h:2.85,showLegend:false,showValue:true,showTitle:false,chartColors:['D4F28B'],showMarker:true,markerSize:8,lineSize:3,catAxisLabelColor:'B4BDB0',catAxisLabelFontSize:12,valAxisLabelColor:'B4BDB0',valAxisLabelFontSize:10,valAxisMinVal:0,valAxisMaxVal:30,valAxisMajorUnit:10,valGridLine:{color:'354131',width:.7},dataLabelColor:'F5F7EE',dataLabelPosition:'t',showBorder:false,showCatName:false,showSerName:false,chartArea:{fill:{color:'111512'}},plotArea:{fill:{color:'111512'}}});pitFoot(s,4);note(s,'Source: examples/data.json pitch; all synthetic. 18/24=75%. Native chart, embedded data workbook. Four fictional months are not historical traction.');
 s=p.addSlide();s.background={color:'D4F28B'};text(s,'ПРЕДЛАГАЕМЫЙ ЗАПРОС',.6,.5,12,.35,12,'3D5E2C',{charSpacing:2,bold:true});text(s,'€600k',.6,1.35,11.8,1.55,88,'111512',{bold:true});text(s,'Чтобы проверить платящий спрос',.7,3.14,11.7,.8,28,'23331D',{bold:true});
 let start=.7;const widths=[5.975,3.585,2.39];['Продукт\n50%','Пилоты\n30%','Инфраструктура\n20%'].forEach((label,i)=>{rect(s,start,4.6,widths[i]-.08,.34,['111512','4B6A36','88A959'][i]);text(s,label,start,5.22,widths[i]-.17,.85,15,'23331D',{bold:true,vertAnchor:'top'});start+=widths[i];});footer(s,5,'УСЛОВНЫЙ БЮДЖЕТ · НЕ ПРЕДЛОЖЕНИЕ ОБ ИНВЕСТИРОВАНИИ','3D5E2C');note(s,'Fictional funding request €600,000. Allocation 50%+30%+20%=100%; €300k/€180k/€120k. No financial forecast provided.');
 s=p.addSlide();s.background={color:'111512'};text(s,'СЛЕДУЮЩИЙ ШАГ',.6,.5,10,.35,12,'D4F28B',{charSpacing:2});text(s,'Сначала —\nдоказать спрос.',.6,1.45,11.8,1.7,48,'F5F7EE',{bold:true});text(s,'Интервью → платный пилот → решение о продукте',.65,4.15,11.6,.65,22,'D4F28B');text(s,'Пока не проверены: размер рынка, готовность платить,\nсебестоимость обслуживания и экономика привлечения.',.65,5.35,11.8,.85,16,'B4BDB0');pitFoot(s,6);note(s,'Explicit limitations: no validated market, business model, team credentials or commercial traction. This is a six-slide art-direction test, not an investment-ready pitch.');
 await p.writeFile({fileName:path.join(out,'02-pitch.pptx')});
}

const B={paper:'F1E9DB',ink:'40392F',muted:'7D7164',clay:'B86D4D',sand:'D7C1A3',dark:'4E5846'};
function bt(s,t,x,y,w,h,size=34,color=B.ink,opt={}){text(s,t,x,y,w,h,size,color,{fontFace:'DejaVu Serif',...opt});}
function brandFoot(s,i,color=B.muted){footer(s,i,'ТИХО / ВЫМЫШЛЕННЫЙ БРЕНД · ГРАФИКА И СГЕНЕРИРОВАННЫЕ ВИЗУАЛЫ',color);}
function artwork(s,x,y,scale=1){
 circle(s,x+.12*scale,y+2.85*scale,4.45*scale,.42*scale,B.ink,{fill:{color:B.ink,transparency:88}});
 s.addShape('arc',{x:x+.45*scale,y:y+.75*scale,w:3.45*scale,h:2.7*scale,rotate:180,adjustPoint:.4,line:{color:B.clay,width:2},fill:{color:B.clay}});
 // Vessel: deliberately graphic, never presented as a photograph or a real product.
 rect(s,x+1.12*scale,y+1.25*scale,2.2*scale,1.55*scale,B.clay);
 circle(s,x+1.12*scale,y+2.34*scale,2.2*scale,.84*scale,B.clay);
 circle(s,x+1.12*scale,y+1.03*scale,2.2*scale,.47*scale,'89533D');
 circle(s,x+1.29*scale,y+1.1*scale,1.86*scale,.28*scale,'5C4233');
 circle(s,x+.05*scale,y+2.18*scale,1.3*scale,.95*scale,B.sand);
 circle(s,x+3.23*scale,y+1.9*scale,.9*scale,1.23*scale,B.dark);
}
async function brand(){const p=deck('ТИХО — визуальный мир бренда','DejaVu Serif');let s;
 const hero=path.join(__dirname,'../examples/assets/quiet-ceramics.png');
 s=p.addSlide();s.background={color:B.paper};s.addImage({path:hero,x:0,y:0,w:W,h:H});text(s,'СТУДИЯ ПРЕДМЕТНОЙ КУЛЬТУРЫ',.65,.45,9,.35,10,B.ink,{charSpacing:1.7});
 bt(s,'тихо',.65,1.37,6.1,1.85,110,B.ink);bt(s,'Форма паузы',.75,4.35,5.5,.85,31);text(s,'Концепция визуальной идентичности\n22 октября 2026',.8,5.6,5.5,.7,13,B.ink);brandFoot(s,1,B.ink);note(s,'Fictional brand. Generated concept image, not a real product photograph. Created with OpenAI image generation on 2026-10-22. Native editable typography over raster image.');
 s=p.addSlide();s.background={color:B.dark};text(s,'ИДЕЯ',.7,.5,10,.35,10,'D8D9C9',{charSpacing:2});bt(s,'Меньше шума.\nБольше\nприсутствия.',.7,1.45,11.5,3.6,49,'F1E9DB');line(s,.8,6.25,3.1,'CDD0BE');brandFoot(s,2,'D8D9C9');note(s,'Creative brand positioning; not a factual or therapeutic claim.');
 s=p.addSlide();s.background={color:B.paper};text(s,'ВИЗУАЛЬНЫЙ СЛОВАРЬ',.7,.45,10,.35,10,B.muted,{charSpacing:1.7});bt(s,'Три ощущения',.7,1.13,11.8,.9,38);
 const xs=[.7,4.9,9.1],labels=['Матовая глина','Мягкая бумага','Тёплая тень'];
 xs.forEach((x,i)=>{rect(s,x,2.55,3.55,2.8,[B.clay,'E3D4BB',B.dark][i]);if(i===0){for(let j=0;j<7;j++)line(s,x+.3,2.95+j*.28,2.95,'CC8C6F',.5);}if(i===1){rect(s,x+.37,2.95,2.4,1.8,'F8F1E4');line(s,x+.56,4.35,1.5,B.sand,.5);}if(i===2){circle(s,x+.5,2.92,2.4,1.75,'79816A');circle(s,x+1.3,3.6,1.85,1.25,'3F4938');}bt(s,labels[i],x,5.7,3.65,.5,18);});brandFoot(s,3);note(s,'Original color/material abstractions. These are visual cues, not material samples or external photography.');
 s=p.addSlide();s.background={color:'D7C1A3'};s.addImage({path:hero,x:.55,y:1.3,w:7.3,h:4.108});text(s,'ВИЗУАЛИЗАЦИЯ КОНЦЕПЦИИ / AI',.65,5.75,7,.3,9,B.ink,{charSpacing:1});text(s,'ОБЪЕКТ / 01',8.5,.7,4,.35,10,B.ink,{charSpacing:1.5});bt(s,'Место\nдля тишины',8.3,2.25,4.35,1.8,32);text(s,'Простая форма.\nНеровный край.\nПауза в повседневности.',8.4,4.68,4.2,1.2,17,B.ink);brandFoot(s,4,B.ink);note(s,'Generated concept still life, not documentary photography. Image is raster; typography remains editable. No product specifications or manufacturing claims.');
 s=p.addSlide();s.background={color:B.paper};text(s,'ЯЗЫК БРЕНДА',.7,.45,10,.35,10,B.muted,{charSpacing:1.7});bt(s,'Спокойствие\nв каждом касании.',.7,1.4,7,1.8,37);
 rect(s,8.5,.95,3.75,5.4,'F8F2E8');rect(s,8.85,1.3,3.05,4.7,'D7C1A3');bt(s,'тихо',9.1,2.3,2.65,.8,36);text(s,'ОСТАВЬТЕ МЕСТО\nДЛЯ ПАУЗЫ',9.1,4.45,2.55,.75,12,B.ink,{charSpacing:1.2});text(s,'Редакционная типографика\nТактильная палитра\nСвободное поле вокруг объекта',.8,4.3,7.1,1.25,17,B.muted);brandFoot(s,5);note(s,'Original concept application on a paper card; native editable text and shapes.');
 s=p.addSlide();s.background={color:B.clay};bt(s,'Оставить\nпространство.',.7,1.3,11.8,2.25,56,'FFF4E5');text(s,'ТИХО / ФОРМА ПАУЗЫ',.8,5.35,11.5,.4,13,'FFF4E5',{charSpacing:2});text(s,'Концепция для проверки арт-дирекшна.\nПредметный визуал сгенерирован; текст и графика редактируются.',.8,6.1,11.5,.65,11,'FFF4E5');brandFoot(s,6,'FFF4E5');note(s,'Original concept. Generated image plus native text and shapes. No unlicensed reference imagery included.');
 await p.writeFile({fileName:path.join(out,'03-brand.pptx')});
}

(async()=>{await strategy();await pitch();await brand();fs.writeFileSync(path.join(out,'build.json'),JSON.stringify({created:'2026-10-22',decks:3,slides:18,data:'studio/examples/data.json',synthetic:true,renderer:'PptxGenJS',purpose:'Acceptance samples, not finished research'},null,2));console.log(out);})().catch(e=>{console.error(e);process.exit(1)});
