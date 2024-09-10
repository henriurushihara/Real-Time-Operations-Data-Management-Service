
--package spec

CREATE OR REPLACE PACKAGE Get_ODM_Data_Pkg AS 
  PROCEDURE Get_Division_List(p_json OUT CLOB);
  PROCEDURE Get_Division_Summary_Data(p_json OUT CLOB);
  PROCEDURE Get_Well_Summary_Data(p_well_id IN NUMBER, p_division_id IN NUMBER, p_json OUT CLOB);
  PROCEDURE Get_Well_Summary_By_Day(p_well_id IN NUMBER, p_division_id IN NUMBER, p_json OUT CLOB);
END Get_ODM_Data_Pkg;
