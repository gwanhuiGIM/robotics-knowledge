---
title: "레이아웃 태그 시험"
category: Systems
content_mode: new_answer
published: 2026-11-08
summary: "ChatGPT 레이아웃 태그 렌더러 회귀 시험용 샘플"
tags: [test]
---
# 레이아웃 태그 시험

<box border radius="xl" padding={3} gap={2}>
  <text color="secondary" weight="medium" size="xs">파이프라인 제목</text>
  <row align=center justify="between">
    **CI 단계**
    <badge>Integration</badge>
  </row>
  <grid columns={3} gap={2}>
    {#each [{name:"빌드",icon:"hammer"},{name:"테스트",icon:"check-check"},{name:"코드 검사",icon:"scan-search"}] as item}
      <grid-item>
        <box background="surface" radius="md" padding={2} align=center>
          <icon name={item.icon}/>
          <text size="xs">{item.name}</text>
        </box>
      </grid-item>
    {/each}
  </grid>
  <box background="rgba(30,110,200,0.07)" border={{size:1,color:"rgba(30,110,200,0.2)"}} width="100px">
    색 상자 $v=\omega r$
    <caption>설명 글자</caption>
  </box>
  <box background="red;position:fixed" width="100px;position:fixed">
    나쁜 속성 <script>alert(1)</script> <img src=x onerror="alert(2)">
  </box>
  <divider color="subtle"/>
  <WritingBlock id="1" variant="standard">예시 문장 **강조**</WritingBlock>
  <Link url="javascript:alert(3)" title="나쁜 링크"/>
  <sparkle size="lg">모르는 태그 안 글자</sparkle>
</box>

본문 링크: <Link url="https://example.com/doc" title="예시 문서"/> 끝.

```html
<box gap={3}>코드 블록 안 태그는 그대로</box>
```

<box align={[]} justify={{x:1}}>
  잘못된 속성 타입
</box>

<box>
```html
<icon name="hammer"/>
```
</box>

- ```html
  <box>목록 안 코드 블록</box>
  ```

인라인 코드 `<Link url="https://example.com/raw" title="코드 안 링크"/>` 그대로.

<box>
## 상자 안 제목
상자 안 내용
</box>

<row>
{#each [{name:"a,b:c"}] as item}<text>{item.name}</text>{/each}
</row>

<row>
  열린 행

후속 일반 문단도 살아 있어야 함

<box gap={2}>
  닫히지 않은 블록 원문

## 다음 절

닫히지 않은 블록 뒤 문단도 살아 있어야 함
