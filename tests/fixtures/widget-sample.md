---
title: "ChatGPT 위젯 태그 시험"
category: Systems
content_mode: original_qa
published: 2026-11-14
summary: "Entity·Cite·AsyncImage·Chart 처리 시험용 fixture"
---

# 위젯 시험

블록 밖 문단 **굵게**입니다. <Cite refs={["turn1search0","turn1search2"]}/>

블록 밖 개체 <Entity category="product" value="Out*Side Robot" disambig="x"/> 끝.

<box>
  특수문자 <Entity value="Lt&Gt <b>"/> 끝
</box>

<row align=start gap={3}>
  <AsyncImage query="robot arm" aspectRatio="4:5" maxWidth="180px"/>
  <box flex="1" gap={2}>
    **<Entity category="product" value="Anvil Robotics OpenYAM" disambig="desc"/>**

    들여쓴 설명 문단입니다. <Cite ref="turn2view0"/>
  </box>
</row>

<AsyncImageGroup query={["robot a","robot b"]}/>

<box gap={2}>
  <Chart content={{"chartType":"bar","meta":{"footer":"자료: 예시 <b>"},"xKey":"model","series":[{"dataKey":"seconds","label":"개입 간격","valueSuffix":"초"}],"data":[{"model":"1세대","seconds":22.6},{"model":"Sage","seconds":340.3}]}}/>
  <caption>캡션 글자 <Cite ref="turn3view0"/></caption>
</box>

`<Cite ref="code"/>` 인라인 코드 안은 그대로.
