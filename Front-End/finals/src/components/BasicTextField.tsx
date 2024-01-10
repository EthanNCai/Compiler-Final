import React, { useState } from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import { Button, Container, Paper, Stack, Typography } from "@mui/material";

export default function BasicTextFields() {
  const [text, setText] = useState<string>("");
  const [resText, setResText] = useState<string>("分析信息将会显示在这里~");
  const [isAnalysisButtonActive, setIsAnalysisButtonActive] =
    useState<boolean>(false);
  const [isGenerateButtonActive, setIsGenerateButtonActive] =
    useState<boolean>(false);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = event.target;
    setText(value);
  };

  const handleBuildAnalysisTable = () => {
    setTimeout(() => {
      setIsAnalysisButtonActive(true);
      setIsGenerateButtonActive(true);
    }, 800);
  };
  const handleAnalysis = () => {
    fetch("http://127.0.0.1:8000/api/parse", {
      method: "POST",
      headers: {
        "Content-Type": "text/plain", // 修改为纯文本形式
      },
      body: text,
    })
      .then((response) => response.text()) // 从响应中获取文本
      .then((data) => {
        setResText(data); // 将响应文本保存到状态中
      })
      .catch((error) => {
        console.error("Failed to analyze:", error);
      });
  };
  const handelExcel = () => {
    fetch("http://127.0.0.1:8000/api/get_analysis_table")
      .then((response) => response.blob())
      .then((blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "analysis_table.xlsx"; // 设置要保存的文件名
        a.click();
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  //get_analysis_table

  return (
    <Container
      sx={{
        display: "flex",
        justifyContent: "center",
        minWidth: "60%",
      }}>
      <Stack>
        <Typography variant="h6" marginTop={"15px"}>
          {"基于LR(1)的PL0文法代码分析器"}
        </Typography>
        <Typography variant="caption" marginBottom={"15px"}>
          {"作者：蔡俊志、涂江得、李伟佳"}
        </Typography>

        <TextField
          id="filled-multiline-flexible"
          label="输入PL0 代码"
          multiline
          minRows={10}
          maxRows={20}
          variant="filled"
          value={text} // 绑定输入框的值
          onChange={handleInputChange} // 处理输入框值的变化
        />
        <Paper sx={{ minWidth: "50%", marginTop: "15px" }}>
          {" "}
          <Typography margin={"10px"}>{resText}</Typography>{" "}
        </Paper>

        <Stack direction={"row"} margin={"10px"}>
          <Button
            variant="contained"
            sx={{ marginX: "5px" }}
            onClick={handleBuildAnalysisTable}>
            建立分析表
          </Button>
          <Button
            variant="contained"
            onClick={handleAnalysis}
            sx={{ marginX: "5px" }}
            disabled={!isAnalysisButtonActive}>
            分析
          </Button>
          <Button
            variant="outlined"
            onClick={handelExcel}
            sx={{ marginX: "5px" }}
            disabled={!isGenerateButtonActive}>
            生成并下载分析表
          </Button>
        </Stack>
      </Stack>
    </Container>
  );
}
