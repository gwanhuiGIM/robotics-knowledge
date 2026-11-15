---
title: "로봇 공정 자동화에서 BC·DAgger·OpenYAM·LBM의 역할"
category: Embodied AI
content_mode: original_qa
published: 2026-11-14
summary: "BC·DAgger 데이터 수집과 티치펜던트의 관계, OpenYAM 플랫폼, Walden LBM의 현장 적용 구상을 정리한 원문 Q&A."
tags: [BC, DAgger, OpenYAM, Walden, LBM, 모방학습]
keywords: "Behavior Cloning Dataset Aggregation 티치펜던트 teleoperation 원터치 공정 자동화"
---

> [!PROMPT]
> 공정의 자동화 도입을 위해, BC 및 DAgger 데이터 수집한다는 것의 의미와 용어 설명. 기존 티치펜던트의 역할을 BC로 대체하는게 되는건지? 예시로 원터치 버튼처럼 만들어 판다는데, open yam이 그 예시인지? 또한 WALDEN의 IBM(LBM?)의 아이디어 제안점 설명해줘

# 로봇 공정 자동화에서 BC·DAgger·OpenYAM·LBM의 역할

핵심은 **로봇의 동작을 사람이 일일이 프로그래밍하는 방식에서, 사람이 작업을 시연하고 로봇이 그 행동을 학습하는 방식으로 전환하는 것**입니다.

이러한 접근을 모방학습(Imitation Learning) 또는 시연 기반 학습(Learning from Demonstration, LfD)이라고 합니다.

다만 BC와 DAgger는 로봇을 가르치는 학습 방법이고, OpenYAM은 로봇 하드웨어 및 개발 플랫폼이며, WALDEN의 LBM은 학습한 행동을 여러 작업에 활용하려는 AI 모델입니다.

## 1. 핵심 용어부터 구분

| 용어 | 정식 명칭 | 역할 |
|---|---|---|
| **BC** | Behavior Cloning | 사람의 작업 시연을 학습하여 모방 |
| **DAgger** | Dataset Aggregation | 로봇이 수행 중 실수하는 상황을 추가 학습 |
| **Teleoperation** | 원격 조작 | 사람이 로봇을 조작하면서 시연 데이터 수집 |
| **Policy** | 행동 정책 | 관측 상태를 입력받아 다음 행동을 결정 |
| **OpenYAM** | Anvil Robotics의 로봇 플랫폼 | 조작·시연·AI 모델 검증용 로봇 팔 |
| **LBM** | Large Behavior Model | 여러 작업에 활용할 수 있는 범용 행동 모델 |
| **VLA** | Vision-Language-Action | 이미지·언어 등을 받아 로봇 행동을 생성하는 모델 구조 |

특히 BC와 DAgger는 별개의 경쟁 기술이라기보다는 **BC로 초기 정책을 학습하고, DAgger로 실제 수행 중 발견한 약점을 보완하는 관계**입니다. <Cite refs={["turn436935search0","turn436935search2"]}/>

## 2. BC와 DAgger의 차이

<box gap={3}>
  <row align=start gap={3}>
    <AsyncImage query="industrial collaborative robot arm human hand guiding teaching demonstration manufacturing robot" aspectRatio="5:4" maxWidth="156px"/>
    <box flex="1" gap={1}>
      **BC — 사람이 성공하는 방법을 보여줌**

      예를 들어 작업자가 로봇으로 부품을 집어서 조립 위치에 놓는 시연을 100회 수행합니다. 모델은 카메라 영상, 로봇 관절 상태, 작업자의 조작 명령을 학습하고 비슷한 상황에서 행동을 재현합니다.
    </box>
  </row>
  <divider color="subtle"/>
  <row align=start gap={3}>
    <AsyncImage query="robot arm teleoperation human operator correcting robot pick and place with VR controllers" aspectRatio="5:4" maxWidth="156px"/>
    <box flex="1" gap={1}>
      **DAgger — 로봇이 실패할 때 교정해 줌**

      학습한 로봇이 부품을 잘못 집으려 하거나 위치를 벗어나면 작업자가 개입합니다. 이때의 상태와 올바른 행동을 추가로 수집해 재학습하면서 대응 범위를 확장합니다.
    </box>
  </row>
</box>

두 방식의 가장 중요한 차이는 **어떤 상태에서 데이터를 수집하느냐**입니다.

- BC: 주로 사람이 만든 성공 궤적에서 데이터를 수집
- DAgger: 학습된 로봇이 실제로 방문한 상태에서 전문가의 올바른 행동을 수집

따라서 BC는 익숙한 환경에서 잘 움직이더라도 예상하지 못한 오차가 누적되면 실패하기 쉽고, DAgger는 그러한 상황에 대한 복구 행동을 추가로 학습할 수 있습니다. <Cite refs={["turn436935search49","turn436935search5"]}/>

## 3. BC가 기존 티치펜던트를 대체하는가?

**부분적으로는 맞지만, 엄밀히 말하면 티치펜던트 전체를 대체하는 기술은 아닙니다.**

티치펜던트는 로봇을 설정하고 조작하는 인터페이스이고, BC는 로봇의 행동을 학습하는 알고리즘이기 때문입니다.

### 전통적 자동화와 BC 기반 자동화의 차이

<box border radius="xl" padding={3} gap={2}>
  <text weight="medium" size="sm">기존 티칭 기반 자동화</text>
  <box background="surface-secondary" radius="md" padding={3} align="center">
    작업자가 좌표·자세·속도·입출력 조건 지정
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" radius="md" padding={3} align="center">
    로봇 프로그램 및 모션 실행
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface" border radius="md" padding={3} align="center">
    정해진 경로와 조건을 반복 수행
  </box>
  <divider/>
  <text weight="medium" size="sm">BC + DAgger 기반 자동화</text>
  <box background="surface-secondary" radius="md" padding={3} align="center">
    사람이 Teleoperation 또는 Hand-guiding으로 시연
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" radius="md" padding={3} align="center">
    카메라·관절·동작 데이터 수집 → BC 모델 학습
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" radius="md" padding={3} align="center">
    학습한 Policy로 작업 실행 → 오류 상황에서 DAgger 교정
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface" border radius="md" padding={3} align="center">
    주변 환경을 관측하면서 행동을 생성·수정
  </box>
</box>

전통적인 로봇 프로그램도 비전 센서, 힘 제어, 조건 분기 등을 활용하면 환경 변화에 대응할 수 있습니다. 차이는 그 대응 규칙을 사람이 명시적으로 구성하느냐, 데이터를 통해 학습하느냐에 있습니다.

| 비교 | 티치펜던트 기반 | BC 기반 |
|---|---|---|
| 동작 생성 | 사전에 정의한 모션·로직 | 학습한 정책의 출력 |
| 물체 위치 변경 | 좌표 보정·비전 로직 등 필요 | 학습 범위 내에서 적응 가능 |
| 신규 작업 | 재티칭·프로그램 수정 | 시연 데이터 수집·모델 적응 |
| 반복 정밀도 | 결정론적 제어에 유리 | 모델·센서·제어기에 의존 |
| 안전·설정 | 티칭 및 안전 기능 활용 | 기존 로봇 안전·제어 시스템 여전히 필요 |

### 원터치 버튼으로 공정을 실행한다는 의미

이는 충분히 가능한 제품 형태입니다. 다만 **원터치 실행 자체가 BC의 특징은 아닙니다.** 기존 로봇도 버튼 하나로 사전 티칭된 프로그램을 실행할 수 있습니다.

BC 기반 제품의 차별점은 버튼 이후의 실행 방식입니다.

예를 들어 작업자가 HMI의 `부품 분류 시작` 버튼을 누르면, AI가 카메라로 부품의 상태를 인식하고 매 순간 적절한 동작을 생성하여 로봇에 전달합니다.

작업 종류에 따라서는 `부품 조립`, `공작기계 투입`, `완성품 정리` 같은 스킬을 선택하는 인터페이스가 될 수도 있습니다.

즉, 제품이 판매하는 가치는 버튼이 아니라 **로봇 스킬의 재사용성, 작업 전환 비용 감소, 환경 변화에 대한 대응 능력**입니다.

---

## 4. OpenYAM은 이런 개념의 예시인가?

<row align="start" gap={3}>
  <AsyncImage query="Anvil Robotics OpenYAM six axis desktop robot arm official product" aspectRatio="4:5" maxWidth="180px"/>
  <box flex="1" gap={2}>
    **<Entity category="product" value="Anvil Robotics OpenYAM" disambig="오픈소스 데스크톱 로봇 매니퓰레이터"/>**

    네. 다만 원터치 자동화 완제품보다는 **모방학습 기반 로봇 개발·데이터 수집 플랫폼**이라는 표현이 정확합니다.

    OpenYAM은 6축 로봇 팔이며, Anvil의 소프트웨어 스택과 결합해 Teleoperation, 데이터 수집, 학습 및 정책 실행 실험에 활용할 수 있습니다. <Cite refs={["turn784967search2","turn784967search14"]}/>
  </box>
</row>

<AsyncImageGroup query={["Anvil Robotics OpenYAM Quest VR teleoperation robot arms demonstration","Anvil Robotics OpenYAM dual arm tabletop manipulation robot setup"]} aspectRatio="5:3" layout="carousel"/>

Anvil은 Quest 기반 원격 조작, LeRobot 연동, 로봇 제어 등의 개발 환경을 제공합니다. Dimensional의 OpenYAM 튜토리얼에는 로봇을 직접 움직여 시연을 기록하고 ACT(Action Chunking Transformer) 정책을 학습하는 과정도 있습니다. <Cite refs={["turn784967search14","turn784967search15"]}/>

여기서 구분할 점은 다음과 같습니다.

- **OpenYAM:** 실제로 움직이는 로봇 하드웨어
- **Teleop Kit:** 작업자 시연을 수집하는 조작 시스템
- **BC/ACT/DAgger:** 수집한 데이터로 학습하거나 개선하는 알고리즘
- **버튼형 HMI:** 학습한 기능을 현장 작업자가 실행하도록 구성한 사용자 인터페이스

이러한 기술들은 하나의 자동화 제품으로 통합할 수 있지만, OpenYAM을 구매했다고 BC나 DAgger 기반 공정 자동화가 곧바로 완성되는 것은 아닙니다.

---

## 5. WALDEN Robotics의 LBM 아이디어

질문하신 명칭은 IBM이 아니라 **LBM(Large Behavior Model)** 이 맞습니다.

Walden Robotics는 대규모 로봇 행동 모델을 제조·물류 현장에 배치하고, 실제 공정에서 발생하는 경험을 통해 성능을 향상시키는 접근을 추진하고 있습니다.

<row align="start" gap={3}>
  <AsyncImage query="Walden Robotics industrial mobile manipulator robot factory manufacturing" aspectRatio="4:5" maxWidth="176px"/>
  <box flex="1" gap={1}>
    **<Entity category="organization" value="Walden Robotics" disambig="산업용 Physical AI 로봇 기업"/>**

    대표 모델: **LBM 2.0: Sage**

    2026년 11월 11일 공개된 Sage는 47억 개 파라미터와 다양한 출처의 약 10만 시간 데이터로 학습된 멀티모달 로봇 행동 모델입니다. <Cite ref="turn805779view0"/>
  </box>
</row>

Walden의 아이디어에서 특히 중요한 요소는 세 가지입니다.

### ① 여러 작업에 공통으로 활용할 수 있는 기반 모델

기존 BC는 특정 작업 데이터를 중심으로 학습하는 경우가 많습니다. 반면 Walden은 여러 로봇, 사람의 시점 영상, UMI 데이터, 시뮬레이션, 실제 개입 데이터를 결합합니다.

목적은 하나의 작업만 기억하는 모델이 아니라, 집기·옮기기·재파지·정렬·조립 등 서로 다른 작업에서 활용할 수 있는 행동 표현을 학습하는 것입니다.

예를 들어 새로운 조립 공정이 생기면 모든 행동을 처음부터 학습하기보다 기존 모델에 해당 공정의 시연을 추가하여 적응시키는 접근입니다.

### ② 실수할 때 스스로 도움을 요청하는 모델

여기가 Walden의 특히 실용적인 제안입니다.

<box border radius="xl" padding={3} gap={2}>
  <box background="surface-secondary" padding={3} radius="md" align="center">
    <text weight="medium">LBM이 공정 수행</text>
    <caption>카메라·상태·작업 지시를 기반으로 행동 생성</caption>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" padding={3} radius="md" align="center">
    <text weight="medium">도움이 필요한지 판단</text>
    <caption>모델 내부의 Call-for-Help 결정 기능</caption>
  </box>
  <grid columns={2} gap={2}>
    <grid-item>
      <box border radius="md" padding={2} align="center" gap={1}>
        <icon name="check-circle" color="success"/>
        <text weight="medium" size="xs">자율 수행 가능</text>
        <text size="xs" color="secondary" textAlign="center">작업 계속 진행</text>
      </box>
    </grid-item>
    <grid-item>
      <box border radius="md" padding={2} align="center" gap={1}>
        <icon name="hand" color="secondary"/>
        <text weight="medium" size="xs">도움 필요</text>
        <text size="xs" color="secondary" textAlign="center">원격 작업자 개입</text>
      </box>
    </grid-item>
  </grid>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" padding={3} radius="md" align="center">
    <text weight="medium">개입 데이터 수집 → 모델 재학습·검증</text>
    <caption>실제 생산 현장의 경험으로 정책 개선</caption>
  </box>
</box>

Walden은 로봇의 행동을 생성하는 헤드(Action Head) 외에 도움 요청 여부를 판단하는 별도 헤드를 공동 학습시킨다고 설명합니다. 이는 단순한 오류 발생 후 정지 로직과는 다릅니다. <Cite ref="turn895311view1"/>

DAgger와 철학적으로 유사하지만, Walden의 기술 전체를 고전적인 DAgger와 동일하다고 볼 수는 없습니다. 사람의 개입 시점 판단, 원격 관제, 대규모 데이터 관리, 멀티모달 학습이 통합되어 있기 때문입니다.

### ③ 현장 데이터를 통해 지속적으로 개선

Walden이 2026년 11월 발표한 실험 결과를 보면 접근의 효과를 좀 더 구체적으로 이해할 수 있습니다.

<box gap={2}>
  <text weight="medium" size="sm">자동차 캠샤프트 공정의 평균 작업자 개입 간격(MTBI)</text>
  <Chart content={{"chartType":"bar","meta":{"footer":"자료: Walden Robotics, 2026-11-11. 동일 작업에 대한 회사 발표 수치."},"xKey":"model","series":[{"dataKey":"seconds","label":"개입 간격","valueSuffix":"초"}],"yAxisMin":0,"data":[{"model":"1세대","seconds":22.6},{"model":"2세대","seconds":78.5},{"model":"Sage","seconds":340.3}]}}/>
  <caption>MTBI(Mean Time Between Interventions)는 작업자가 개입해야 하는 사건 사이의 평균 시간입니다. 길수록 작업자 도움 없이 연속 수행하는 시간이 길다는 의미입니다. <Cite ref="turn805779view0"/></caption>
</box>

다른 7개 작업에 대한 비교 실험에서는 Sage가 작업별 평균 6.2시간의 시연 데이터로 적응하고, 이후 교정 데이터를 활용해 평균 자율 수행 비율 약 89%에 도달했다고 발표했습니다.

이는 Walden이 공개한 자체 평가 결과이며, 모든 제조 공정에서 그 성능이 보장된다는 뜻은 아닙니다. <Cite ref="turn805779view0"/>

중요한 것은 **로봇이 생산에 참여하는 과정 자체가 추가 학습 데이터를 생산하도록 설계했다는 점**입니다.

## 6. 실제 공정 자동화에 적용한다면?

기존에 경험한 두산 M0609, ROS 2, MoveIt 2, RealSense D435i 등을 기준으로 보면 다음처럼 구현 방향을 구분할 수 있습니다.

| 구현 방식 | 핵심 기술 | 적합한 공정 |
|---|---|---|
| 기존 자동화 | 티칭, MoveIt, PLC, FSM | 위치가 고정된 단순 반복 작업 |
| BC 기반 | Teleop, 카메라, 시연 데이터, Policy | 물체 위치나 자세가 조금씩 달라지는 작업 |
| BC + DAgger | BC + 작업자 개입 및 재학습 | 예외 상황이 자주 발생하는 작업 |
| LBM 기반 | 사전학습 모델 + 현장 적응 + 원격 개입 | 공정 변경이 많고 여러 작업을 수행하는 환경 |

### 예시: M0609 부품 투입 공정

<list marker="number" gap={2}>
  <list-item>**데이터 수집 환경 구축** — D435i RGB 영상, 관절 상태, 그리퍼 상태, 작업자 명령을 타임스탬프와 함께 기록합니다.</list-item>
  <list-item>**BC 학습** — Hand-guiding 또는 Teleoperation으로 다양한 초기 위치에서 집기·투입 시연을 수집합니다.</list-item>
  <list-item>**정책 실행** — 학습한 모델이 현재 영상과 로봇 상태를 입력받아 다음 행동을 생성합니다.</list-item>
  <list-item>**DAgger 보완** — 로봇이 잘못 정렬하거나 집는 데 실패하는 상황에서 작업자가 교정하고 해당 데이터를 추가 학습합니다.</list-item>
  <list-item>**원터치 운영** — 검증된 정책을 HMI 버튼으로 호출하되, 실행 허가·안전 인터록·비상정지·성공 판정은 별도로 구성합니다.</list-item>
</list>

실제로는 BC의 출력이 관절 위치 명령인지, TCP 목표 자세인지, 짧은 행동 시퀀스(Action Chunk)인지에 따라 ROS 2 제어 구조도 달라집니다.

예를 들어 기존 MoveIt 기반 구조를 유지하면서 AI가 목표 자세를 생성하도록 만들 수도 있습니다. 반대로 저수준 행동 정책을 직접 서보 제어에 연결할 수도 있지만, 후자는 실시간성·안전성 검증 부담이 더 큽니다.

여기에서 특히 강조하고 싶은 점은 **BC/DAgger를 도입했다고 별도의 로봇 안전 시스템이나 티치펜던트의 운영·복구 기능이 불필요해지는 것은 아니라는 점**입니다.

## 7. 기술 도입 관점에서의 판단

BC/DAgger와 LBM을 비교할 때는 다음처럼 이해하는 것이 적절합니다.

- **BC:** 로봇이 사람의 행동을 학습하게 만드는 기본 방법론
- **DAgger:** 학습한 로봇의 실제 실행 경험을 다시 학습에 활용하는 개선 방법론
- **LBM:** 다양한 작업의 지식과 행동을 공유하는 대규모 정책 모델
- **Walden의 접근:** LBM을 공장에 배치하고, 도움 요청·원격 개입·재학습·검증까지 하나의 운영 체계로 연결하는 것

제가 가장 주목하는 부분은 모델의 크기보다 **자동화 공정의 개발·개선 방식이 바뀐다는 점**입니다.

기존에는 새로운 공정이 들어올 때마다 로봇 엔지니어가 경로, I/O, 조건 분기, 예외 처리 로직을 작성했다면, 앞으로는 현장 작업자의 시연과 개입 데이터를 활용해 로봇 스킬을 만들어가는 비중이 커질 수 있습니다.

다만 모든 공정에 학습 기반 제어가 유리한 것은 아닙니다. 좌표가 고정되고 반복성이 높은 작업이라면 기존 티칭·FSM 방식이 비용과 검증 가능성 측면에서 오히려 우수할 수 있습니다.

반대로 비정형 부품, 복잡한 파지, 자주 변경되는 생산 품목, 사람이 개입해야 하는 예외 상황이 많은 공정에서는 BC·DAgger·LBM의 가치가 높아집니다.

**관련 기술 자료**

- <Link url="https://docs.dimensional.org/capabilities/manipulation/learning/tutorials/openyam-hand-teaching/" title="OpenYAM 시연 데이터 수집 및 ACT 학습 튜토리얼"/>
- <Link url="https://github.com/SRA-VJTI/karma" title="Karma — Teleop·Policy 실행·DAgger 오픈소스 구현"/>
- <Link url="https://www.waldenrobotics.com/news/lbm-2-0-accelerating-learning-in-deployment" title="Walden LBM 2.0: Sage 기술 발표"/>
- <Link url="https://www.waldenrobotics.com/news/call-for-help-teaching-robots-to-request-assistance" title="Walden의 로봇 도움 요청 및 현장 학습 구조"/>

---

확신도: 검증됨(BC·DAgger의 정의, OpenYAM의 역할, Walden LBM 2.0의 공개 기술·평가 결과 확인) / 추론(M0609 적용 아키텍처 및 도입 전략)
내가 채워넣은 가정: 원터치 버튼은 공정 실행용 HMI를 의미하며, 기존 M0609 환경을 실제 적용 예시로 사용
확인 요청: 없음
