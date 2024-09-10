
--package body

CREATE OR REPLACE PACKAGE BODY Get_ODM_Data_Pkg AS 

  PROCEDURE Get_Division_List(p_json OUT CLOB) IS
  BEGIN
    SELECT JSON_ARRAYAGG(
             JSON_OBJECT(
               'Division_Id' VALUE DIVISION_ID,
               'Division_Name' VALUE DIVISION_NAME
             )
           ).TO_CLOB() INTO p_json
    FROM odm_division
    WHERE division_name IS NOT NULL
    ORDER BY Division_Id;
  END Get_Division_List;

  PROCEDURE Get_Division_Summary_Data(p_json OUT CLOB) IS
  BEGIN
    SELECT JSON_ARRAYAGG(
             JSON_OBJECT(
               'Division_Id' VALUE DIVISION_ID,
               'Division_Name' VALUE DIVISION_NAME,
               'Well_Count' VALUE WELL_COUNT,
               'Total_Oil_Produced' VALUE TOTAL_OIL_PRODUCED,
               'Total_Budget' VALUE TOTAL_BUDGET,
               'Total_Actual' VALUE TOTAL_ACTUAL,
               'Total_Oil_Sales' VALUE TOTAL_OIL_SALES
             )
           ).TO_CLOB() INTO p_json
    FROM Get_Division_Summary_Data_MV
    ORDER BY Division_Id;
  END Get_Division_Summary_Data;

  PROCEDURE Get_Well_Summary_Data(p_well_id IN NUMBER, p_division_id IN NUMBER, p_json OUT CLOB) IS
  BEGIN
    SELECT JSON_ARRAYAGG(
             JSON_OBJECT(
               'well_id' VALUE WELL_ID,
               'well_name' VALUE WELL_NAME,
               'division_id' VALUE DIVISION_ID,
               'division_name' VALUE DIVISION_NAME,
               'total_oil_produced' VALUE TOTAL_OIL_PRODUCED,
               'total_budget' VALUE TOTAL_BUDGET,
               'total_actual' VALUE TOTAL_ACTUAL,
               'total_oil_sales' VALUE TOTAL_OIL_SALES
             )
           ).TO_CLOB() INTO p_json
    FROM Get_Well_Summary_Data_MV
    WHERE well_id = p_well_id AND division_id = p_division_id;
  END Get_Well_Summary_Data;

  PROCEDURE Get_Well_Summary_By_Day(p_well_id IN NUMBER, p_division_id IN NUMBER, p_json OUT CLOB) IS
    l_temp CLOB;
    l_chunk VARCHAR2(4000);
    l_json_start VARCHAR2(4000) := '[';
    l_json_end VARCHAR2(4000) := ']';
    l_comma VARCHAR2(1) := ',';
    l_first BOOLEAN := TRUE;
  BEGIN
    -- Initialize the CLOB
    dbms_lob.createtemporary(l_temp, TRUE);

    FOR rec IN (SELECT WELL_ID, WELL_NAME, DIVISION_ID, DIVISION_NAME, DATE_VALUE, NVL(OIL_PRODUCED, 0) AS OIL_PRODUCED, OIL_PRICE, NVL(OIL_SALES, 0) AS OIL_SALES
                FROM Get_Well_Summary_By_Day_VW
                WHERE well_id = p_well_id AND division_id = p_division_id) LOOP

      -- Create JSON object
      l_chunk := '{' ||
                 '"well_id":' || rec.WELL_ID || ',' ||
                 '"well_name":"' || rec.WELL_NAME || '",' ||
                 '"division_id":' || rec.DIVISION_ID || ',' ||
                 '"division_name":"' || rec.DIVISION_NAME || '",' ||
                 '"date_value":"' || TO_CHAR(rec.DATE_VALUE, 'YYYY-MM-DD') || '",' ||
                 '"oil_produced":' || rec.OIL_PRODUCED || ',' ||
                 '"oil_price":' || rec.OIL_PRICE || ',' ||
                 '"oil_sales":' || rec.OIL_SALES ||
                 '}';

      -- Append JSON object to the CLOB
      IF l_first THEN
        l_first := FALSE;
      ELSE
        dbms_lob.append(l_temp, l_comma);
      END IF;
      dbms_lob.append(l_temp, l_chunk);
    END LOOP;

    -- Add JSON array brackets
    dbms_lob.append(p_json, l_json_start);
    dbms_lob.append(p_json, l_temp);
    dbms_lob.append(p_json, l_json_end);

    -- Free temporary CLOB
    dbms_lob.freetemporary(l_temp);
  END Get_Well_Summary_By_Day;

END Get_ODM_Data_Pkg;
