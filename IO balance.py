#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy
import datetime

# 파일 불러오기
path = ''

# 시간까지 동일한 중복데이터 제거
df = pd.read_excel(path, dtype=str, skiprows=1).replace('총배설량+총배액량', '총배설량')
dfdrop = df.drop_duplicates(subset=['환자번호','간호항목/진술문명','[간호기록]기록작성일시','Value'])

# 날짜 추출
df['date'] = df['[간호기록]기록작성일시'].str.split(' ').str.get(0)
df['Value'] = pd.to_numeric(df['Value'])

# 같은 날 기준 총 섭취량 : input
input = df[df['간호항목/진술문명'].isin(['총섭취량','Input'])].groupby(['환자번호','date'], as_index=False).sum()
input.rename(columns = {'Value':'input'}, inplace=True)

# 같은 날 기준 총 배설+배액량 : output
# 시간끼리의 최댓값 추출, 이 최댓값을 날짜별 총합 계산
dfoutput = df[df['간호항목/진술문명'].isin(['총배설량','총배액량'])].groupby(['환자번호','[간호기록]기록작성일시'], as_index=False).max()
output = dfoutput[dfoutput['간호항목/진술문명'].isin(['총배설량','총배액량'])].groupby(['환자번호','date'], as_index=False).sum()
output.rename(columns = {'Value':'output'}, inplace=True)

# 환자번호, 날짜 기준 병합
merge_outer = pd.merge(input, output, how='outer', on=['환자번호', 'date']).fillna(0)
merge_outer['I/O balance'] = merge_outer['input'] - merge_outer['output']

# 결과 데이터 저장
merge_outer.to_excel('', index=False)

