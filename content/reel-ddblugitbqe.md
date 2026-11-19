---
title: "전공 세부 분야보다 컴퓨터 과학 기초부터 — CSE 학습 로드맵"
category: Reels
content_mode: new_answer
published: 2026-11-19
summary: "CSE 세부 전공·언어 선택보다 문제 해결력과 컴퓨터 과학 기초(자료구조·DB·API·전공 과목·시스템 설계)를 먼저 다지라는 릴스를 화면 기준으로 정리하고, 배울 점과 이어 볼 지점을 덧붙였습니다."
card_label: "Instagram 릴스 · CS 기초 · 학습 로드맵"
tags: [Computer Science, DSA, 자료구조, System Design, 학습 로드맵]
keywords: "computer science CSE DSA data structure algorithm DBMS OS CN COA system design C++ Python 자료구조 알고리즘 운영체제 네트워크 학습로드맵 영상요약 reels"
source_note: "출처: Instagram @codewithnishchal 릴스(2026-09-08) https://www.instagram.com/reel/DdBlUGiTBqe/ — 영상은 옮기지 않고 요약과 장면 캡처 일부만 둔다"
---

> [!NOTE]
> 이 글은 ChatGPT 원문 Q&A가 아니라, Claude가 Instagram 릴스를 보고 새로 정리한 글입니다. 확보한 것: 캡션, 영상 화면(약 1분 30초, 3초 간격 장면 30장 확인). 확보 못 한 것: **음성(받아쓰기 도구 미설치 — 음성 미반영)**. 그래서 "릴스 요약"은 화면에 보이는 마인드맵 글자와 캡션만 근거로 했고, 화자가 말로 설명한 내용은 반영하지 않았습니다. 장면 캡처 3장은 출처 표기 인용이며 원작자 허락은 받지 않았습니다. 화자 얼굴이 나오는 아래쪽은 잘라 내고 마인드맵 부분만 실었습니다. 질문 원문 없이 링크만 받아 정리한 글입니다.

## 릴스 요약

@codewithnishchal(2026-09-08 게시, 약 1분 30초). **영상이 말하려는 것**: 세부 전공(specialisation)을 고르기 전에 컴퓨터 과학 자체를 먼저 배우라는 것. 캡션의 핵심 문장은 다음과 같습니다.

> "Focus on learning computer science first not the specialisation."
> "When your problem-solving skills get strong, you can grind anything you want later on."

화면 위쪽의 마인드맵에 손글씨로 표시를 더해 가며 설명하고, 화면은 세 장면으로 이어집니다.

**1. CSE 세부 전공 (0:00~0:27)** — 왼쪽의 `CSE` 노드에서 `CSE + AI`, `CSE + Data Science`, `CSE + Cyber security`, `CSE + Cloud Computing`, `CSE + IOT`, `CSE + Big Data`, `Information Technology` 일곱 갈래가 뻗어 있고, 화자가 각 갈래에 밑줄과 괄호를 긋습니다. 캡션의 "specialisation"이 이 갈래들에 해당하는 것으로 보입니다(음성 미확인).

![CSE에서 일곱 세부 전공으로 갈라지는 마인드맵 — 출처 @codewithnishchal 릴스 장면 캡처](../assets/img/reel-ddblugitbqe/scene1.jpg)
<text color="secondary" size="xs">출처: @codewithnishchal · https://www.instagram.com/reel/DdBlUGiTBqe/ · 0:02 장면</text>

**2. 언어 (0:27~0:54)** — `Language` 노드 아래 `C`, `C++`, `JAVA`, `Python`, `JavaScript`. 화자는 `C`에 X 표시를 하고, `C++`에 동그라미를 친 뒤 손글씨 `DSA`로 화살표를 잇습니다. `JAVA`·`Python` 옆에도 세로 괄호를 그립니다(그 의미는 음성 없이 확인할 수 없음).

![Language 노드 아래 다섯 언어, C++에서 DSA로 이어지는 손글씨 — 출처 @codewithnishchal 릴스 장면 캡처](../assets/img/reel-ddblugitbqe/scene2.jpg)
<text color="secondary" size="xs">출처: @codewithnishchal · https://www.instagram.com/reel/DdBlUGiTBqe/ · 0:45 장면</text>

**3. 공부 항목 (0:57~1:30)** — 이름 없는 노드 아래 `Logic Building`, `Data Structure`, `Database`, `APIS`, `Coursework`, `System Design`. 화자가 위에서부터 차례로 동그라미·상자를 치고, `Coursework`를 펼치면 `DBMS`, `OS`, `CN`, `AI`, `COA`가 나옵니다(이어서 `Functional`로 시작하는 항목이 잠깐 보이지만 잘려 다 읽히지 않음).

![Logic Building부터 System Design까지 공부 항목, Coursework 아래 DBMS·OS·CN·AI·COA — 출처 @codewithnishchal 릴스 장면 캡처](../assets/img/reel-ddblugitbqe/scene3.jpg)
<text color="secondary" size="xs">출처: @codewithnishchal · https://www.instagram.com/reel/DdBlUGiTBqe/ · 1:16 장면</text>

## 영상에서 배울 점

각 항목은 영상 근거를 먼저 적고, 그 뒤의 풀이는 Claude가 덧붙인 것입니다.

1. **세부 분야는 기초 위에 얹힌다.** 근거: 캡션 첫 문장, 0:00~0:27의 일곱 갈래 중 여섯이 `CSE +` 형태(나머지 하나는 `Information Technology`). 풀이: AI·클라우드·보안 같은 갈래는 이름은 달라도 같은 기초(자료구조, OS, 네트워크, DB)를 공유합니다. 갈래를 바꾸더라도 기초는 그대로 쓰입니다.
2. **공부 순서의 뼈대가 하나의 목록으로 주어진다.** 근거: 0:57~1:30의 `Logic Building → Data Structure → Database → APIS → Coursework → System Design`과 화자가 위에서부터 차례로 표시하는 모습. 풀이: 화면 위쪽일수록 먼저 표시되지만, 이것이 권장 순서라는 말은 음성 없이 확인할 수 없습니다. 그래도 "논리 → 자료구조 → 데이터 저장 → 외부 연결 → 이론 과목 → 전체 설계"로 읽으면 혼자 공부할 때 체크리스트로 쓸 수 있습니다.
3. **언어는 수단이고 DSA와 함께 묶인다.** 근거: 0:27~0:54에서 `C++` → 손글씨 `DSA` 화살표. 풀이: 언어 하나를 골라 자료구조·알고리즘을 직접 구현해 보는 것이 언어 공부와 기초 공부를 한 번에 하는 방법으로 흔히 권해집니다. C에 X 표시를 한 이유는 영상만으로는 알 수 없습니다.
4. **한계.** 캡션은 "문제 해결력이 강해지면 나중에 무엇이든 할 수 있다"고 하지만, 세부 분야마다 따로 익혀야 할 수학·도메인 지식(예: AI의 선형대수·확률)은 이 로드맵에 나오지 않습니다. 기초 우선이라는 방향은 참고하되, 분야별 추가 지식은 따로 챙겨야 합니다.

## 나와 연결되는 지점

- **연관성: 간접.** 영상은 특정 응용 분야가 아니라 컴퓨터 과학 전반의 학습 순서를 다룹니다. 다만 영상 `Coursework`에 나오는 과목은 로보틱스 SW에서도 그대로 쓰입니다(이하 Claude 풀이, 영상에는 로보틱스 언급 없음) — 경로 탐색은 자료구조·알고리즘, 멀티스레드 노드는 OS, 노드 간 통신은 네트워크(CN)에 기대고 있습니다.
- 이 사이트의 이어 볼 글:
  - [로보틱스 경로 탐색·경로 계획 알고리즘 총정리](robotics-path-planning-algorithms.html) — Dijkstra·A* 같은 그래프 탐색이 DSA의 실제 쓰임
  - [멀티스레딩(Multithreading)의 개념과 Python·ROS 2 노드 최적화](python-ros2-multithreading.html) — OS의 스레드·동시성 개념이 쓰이는 곳
  - [로보틱스 신입 SW 개발자에게 요구되는 C++·Python 역량](robotics-junior-sw-cpp-python.html) — 영상의 "언어 + DSA" 묶음을 채용 기준 쪽에서 본 글
- 이어서 공부하면 좋을 주제: 영상 `Coursework`의 OS·CN을 각각 한 편씩 정리하기, `System Design`이 실제로 무엇을 묻는지(구성 요소 분할·확장성) 정리하기.

## 알면 좋을 지식

아래는 Claude가 덧붙인 일반 지식입니다(영상 내용 아님).

| 화면 표기 | 풀이 |
|---|---|
| CSE | Computer Science and Engineering(컴퓨터공학) |
| DSA | Data Structures and Algorithms(자료구조·알고리즘) |
| DBMS | Database Management System(데이터베이스 관리 시스템) |
| OS | Operating System(프로세스·스레드·스케줄링·메모리) |
| CN | Computer Networks(컴퓨터 네트워크) |
| COA | Computer Organization and Architecture(컴퓨터 구조) |
| System Design | 여러 구성 요소를 묶는 전체 구조 설계 |

## 학습 자료

아래는 Claude가 덧붙인 자료입니다(영상에 나오지 않음).

- 자료구조·알고리즘: CLRS *Introduction to Algorithms*(MIT Press, 주소 미확인)
- 운영체제: *Operating Systems: Three Easy Pieces*(OSTEP, 주소 미확인)
- 네트워크: Kurose·Ross *Computer Networking: A Top-Down Approach*(주소 미확인)
- 컴퓨터 구조: Patterson·Hennessy *Computer Organization and Design*(주소 미확인)

## 관련 시뮬레이션·도구

| 도구 | 용도 | 비고 |
|---|---|---|
| VisuAlgo | 자료구조·알고리즘 동작 시각화 | 주소·가격 미확인 |
| LeetCode / 백준 | DSA 문제 풀이 | 가격 미확인 |
