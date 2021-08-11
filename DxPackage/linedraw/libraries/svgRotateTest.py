import svgutils
svg = svgutils.transform.fromfile('output/out.svg')
originalSVG = svgutils.compose.SVG('output/out.svg')
originalSVG.rotate(90)
originalSVG.move(svg.height, 10)

figure = svgutils.compose.Figure(svg.height, svg.width, originalSVG)
figure.save('svgNew.svg')