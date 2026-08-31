$root = "C:\Users\NK-MAL\Documents\SPORTIVA CM"
$defense = Join-Path $root "DEFENSE"
New-Item -ItemType Directory -Force -Path $defense | Out-Null

# Copy the original project files into DEFENSE exactly as they are.
Copy-Item -Force (Join-Path $root "SPORTIVA_CM_DEFENSE_DOCUMENT.docx") (Join-Path $defense "SPORTIVA_CM_DEFENSE_DOCUMENT.docx")
Copy-Item -Force (Join-Path $root "LOCAL_RUN_GUIDE.md") (Join-Path $defense "LOCAL_RUN_GUIDE.md")
Copy-Item -Force (Join-Path $root "SPORTIVA_CM_POWERPOINT_OUTLINE.md") (Join-Path $defense "SPORTIVA_CM_POWERPOINT_OUTLINE.md")

# Build a Word docx based on the original Local Run Guide content.
$docTemp = Join-Path $defense "_docx_temp"
if (Test-Path $docTemp) { Remove-Item $docTemp -Recurse -Force }
New-Item -ItemType Directory -Path $docTemp | Out-Null
New-Item -ItemType Directory -Path (Join-Path $docTemp "word") | Out-Null
New-Item -ItemType Directory -Path (Join-Path $docTemp "docProps") | Out-Null
New-Item -ItemType Directory -Path (Join-Path $docTemp "_rels") | Out-Null

$guide = Get-Content (Join-Path $root "LOCAL_RUN_GUIDE.md") -Raw
$lines = $guide -split "`r?`n"
$paras = ""
foreach ($line in $lines) {
  $safe = $line.Replace("&", "&amp;").Replace("<", "&lt;").Replace(">", "&gt;")
  $paras += "<w:p><w:r><w:t>$safe</w:t></w:r></w:p>"
}
$docXml = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    $paras
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>
"@
Set-Content -Path (Join-Path $docTemp "word\document.xml") -Value $docXml -Encoding UTF8
Set-Content -Path (Join-Path $docTemp "word\styles.xml") -Value '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style></w:styles>' -Encoding UTF8
Set-Content -Path (Join-Path $docTemp "docProps\core.xml") -Value '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>Sportiva CM Local Run Guide</dc:title><dc:creator>GitHub Copilot</dc:creator><cp:lastModifiedBy>GitHub Copilot</cp:lastModifiedBy></cp:coreProperties>' -Encoding UTF8
Set-Content -Path (Join-Path $docTemp "docProps\app.xml") -Value '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Microsoft Office Word</Application></Properties>' -Encoding UTF8
Set-Content -Path (Join-Path $docTemp "_rels\.rels") -Value '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>' -Encoding UTF8
Set-Content -Path (Join-Path $docTemp "[Content_Types].xml") -Value '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>' -Encoding UTF8
if (Test-Path (Join-Path $defense "SPORTIVA_CM_LOCAL_RUN_GUIDE.docx")) { Remove-Item (Join-Path $defense "SPORTIVA_CM_LOCAL_RUN_GUIDE.docx") -Force }
[System.IO.Compression.ZipFile]::CreateFromDirectory($docTemp, (Join-Path $defense "SPORTIVA_CM_LOCAL_RUN_GUIDE.docx"))
Remove-Item $docTemp -Recurse -Force

# Build a basic PowerPoint .pptx using the same project outline content.
$pptTemp = Join-Path $defense "_pptx_temp"
if (Test-Path $pptTemp) { Remove-Item $pptTemp -Recurse -Force }
New-Item -ItemType Directory -Path $pptTemp | Out-Null
New-Item -ItemType Directory -Path (Join-Path $pptTemp "ppt") | Out-Null
New-Item -ItemType Directory -Path (Join-Path $pptTemp "ppt\slides") | Out-Null
New-Item -ItemType Directory -Path (Join-Path $pptTemp "ppt\slideLayouts") | Out-Null
New-Item -ItemType Directory -Path (Join-Path $pptTemp "ppt\slideMasters") | Out-Null
New-Item -ItemType Directory -Path (Join-Path $pptTemp "ppt\theme") | Out-Null
New-Item -ItemType Directory -Path (Join-Path $pptTemp "docProps") | Out-Null
New-Item -ItemType Directory -Path (Join-Path $pptTemp "_rels") | Out-Null
New-Item -ItemType Directory -Path (Join-Path $pptTemp "ppt\_rels") | Out-Null
New-Item -ItemType Directory -Path (Join-Path $pptTemp "ppt\slides\_rels") | Out-Null
New-Item -ItemType Directory -Path (Join-Path $pptTemp "ppt\slideLayouts\_rels") | Out-Null
New-Item -ItemType Directory -Path (Join-Path $pptTemp "ppt\slideMasters\_rels") | Out-Null

$slideXml = @'
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      <p:sp>
        <p:nvSpPr><p:cNvPr id="2" name="Title 1"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="457200" y="274320"/><a:ext cx="8229600" cy="685800"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>
        <p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:r><a:rPr lang="en-US" sz="2800" b="1"/><a:t>SPORTIVA CM</a:t></a:r></a:p></p:txBody>
      </p:sp>
      <p:sp>
        <p:nvSpPr><p:cNvPr id="3" name="TextBox 2"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="457200" y="1371600"/><a:ext cx="8229600" cy="4114800"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>
        <p:txBody><a:bodyPr/><a:lstStyle/>
          <a:p><a:r><a:rPr lang="en-US" sz="1800"/><a:t>• Cameroon sports promotion platform</a:t></a:r></a:p>
          <a:p><a:r><a:rPr lang="en-US" sz="1800"/><a:t>• Clubs, athletes, fans, and sponsors connected</a:t></a:r></a:p>
          <a:p><a:r><a:rPr lang="en-US" sz="1800"/><a:t>• Events, media feed, marketplace, sponsorships</a:t></a:r></a:p>
          <a:p><a:r><a:rPr lang="en-US" sz="1800"/><a:t>• Django-based MVP project</a:t></a:r></a:p>
        </p:txBody>
      </p:sp>
    </p:spTree>
  </p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
</p:sld>
'@
Set-Content -Path (Join-Path $pptTemp "ppt\slides\slide1.xml") -Value $slideXml -Encoding UTF8
Set-Content -Path (Join-Path $pptTemp "ppt\presentation.xml") -Value '<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" saveSubsetFonts="1" autoCompressPictures="0"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst><p:sldIdLst><p:sldId id="256" r:id="rId2"/></p:sldIdLst><p:sldSz cx="12192000" cy="6858000"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>' -Encoding UTF8
Set-Content -Path (Join-Path $pptTemp "ppt\slideMasters\slideMaster1.xml") -Value '<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld name="Office Theme"><p:bg><p:bgPr><a:solidFill><a:schemeClr val="bg1"/></a:solidFill></p:bgPr></p:bg><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/><p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst></p:sldMaster>' -Encoding UTF8
Set-Content -Path (Join-Path $pptTemp "ppt\slideLayouts\slideLayout1.xml") -Value '<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="titleAndContent" preserve="1"><p:cSld name="Title and Content"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/></p:sldLayout>' -Encoding UTF8
Set-Content -Path (Join-Path $pptTemp "ppt\theme\theme1.xml") -Value '<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Office Theme"><a:themeElements><a:clrScheme name="Office"><a:dk1><a:sysClr val="windowText" lastClr="000000"/></a:dk1><a:lt1><a:sysClr val="window" lastClr="FFFFFF"/></a:lt1><a:dk2><a:srgbClr val="1F497D"/></a:dk2><a:lt2><a:srgbClr val="EEECE1"/></a:lt2><a:accent1><a:srgbClr val="4F81BD"/></a:accent1><a:accent2><a:srgbClr val="C0504D"/></a:accent2><a:accent3><a:srgbClr val="9BBB59"/></a:accent3><a:accent4><a:srgbClr val="8064A2"/></a:accent4><a:accent5><a:srgbClr val="4BACC6"/></a:accent5><a:accent6><a:srgbClr val="F79646"/></a:accent6><a:hlink><a:srgbClr val="0000FF"/></a:hlink><a:folHlink><a:srgbClr val="800080"/></a:folHlink></a:clrScheme><a:fontScheme name="Office"><a:majorFont><a:latin typeface="Calibri"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont><a:minorFont><a:latin typeface="Calibri"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont></a:fontScheme><a:fmtScheme name="Office"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst><a:lnStyleLst><a:ln w="9525" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/></a:ln></a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme></a:themeElements><a:objectDefaults/><a:extraClrSchemeLst/></a:theme>' -Encoding UTF8
Set-Content -Path (Join-Path $pptTemp "docProps\core.xml") -Value '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>Sportiva CM Defense Presentation</dc:title><dc:creator>GitHub Copilot</dc:creator><cp:lastModifiedBy>GitHub Copilot</cp:lastModifiedBy></cp:coreProperties>' -Encoding UTF8
Set-Content -Path (Join-Path $pptTemp "docProps\app.xml") -Value '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Microsoft Office PowerPoint</Application></Properties>' -Encoding UTF8
Set-Content -Path (Join-Path $pptTemp "[Content_Types].xml") -Value '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/><Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/><Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/><Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/><Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>' -Encoding UTF8
Set-Content -Path (Join-Path $pptTemp "_rels\.rels") -Value '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>' -Encoding UTF8
Set-Content -Path (Join-Path $pptTemp "ppt\_rels\presentation.xml.rels") -Value '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/presProps" Target="presProps.xml"/><Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/viewProps" Target="viewProps.xml"/><Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/></Relationships>' -Encoding UTF8
Set-Content -Path (Join-Path $pptTemp "ppt\slides\_rels\slide1.xml.rels") -Value '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/></Relationships>' -Encoding UTF8
Set-Content -Path (Join-Path $pptTemp "ppt\slideMasters\_rels\slideMaster1.xml.rels") -Value '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/></Relationships>' -Encoding UTF8
Set-Content -Path (Join-Path $pptTemp "ppt\slideLayouts\_rels\slideLayout1.xml.rels") -Value '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/></Relationships>' -Encoding UTF8
if (Test-Path (Join-Path $defense "SPORTIVA_CM_DEFENSE_PRESENTATION.pptx")) { Remove-Item (Join-Path $defense "SPORTIVA_CM_DEFENSE_PRESENTATION.pptx") -Force }
[System.IO.Compression.ZipFile]::CreateFromDirectory($pptTemp, (Join-Path $defense "SPORTIVA_CM_DEFENSE_PRESENTATION.pptx"))
Remove-Item $pptTemp -Recurse -Force

Write-Output "DEFENSE folder ready."
Get-ChildItem -Name $defense | Sort-Object
