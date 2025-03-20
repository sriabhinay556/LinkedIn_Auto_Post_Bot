parser_logic = """
'''
import json

html_data = '<body><div id="__nuxt"><div><header><nav><a href="/"><img src="/_nuxt/gfi-logo-white.c30e7ffd.svg"/></a><span><span>/</span><span>Scala</span></span></nav></header><main><section><section><div><h3>About</h3><p>Good First Issue cur</p></div><div><h3>Browse by language</h3><div><a href="/language/python">Python<span>× 71</span></a><a href="/language/go">Go<span>× 48</span></a><a href="/language/typescript">TypeScript<span>× 45</span></a><a href="/language/javascript">JavaScript<span>× 45</span></a><a href="/language/cplusplus">C++<span>× 30</span></a><a href="/language/java">Java<span>× 24</span></a><a href="/language/csharp">C#<span>× 18</span></a><a href="/language/rust">Rust<span>× 17</span></a><a href="/language/c">C<span>× 11</span></a><a href="/language/php">PHP<span>× 10</span></a><a href="/language/html">HTML<span>× 7</span></a><a href="/language/ruby">Ruby<span>× 6</span></a><a href="/language/dart">Dart<span>× 4</span></a><a href="/language/scala">Scala<span>× 3</span></a><a href="/language/kotlin">Kotlin<span>× 3</span></a><a href="/language/lua">Lua<span>× 3</span></a></div></div><div><a href="https://github.com/deepsourcelabs/good-first-issue#adding-a-new-project"><svg><path></path></svg><span>Add your project</span></a></div><div><a href="https://deepsource.com?ref=gfi"><svg><path></path></svg><span>A<span>DeepSource</span>initative</span></a></div></section><div><div id="repo-246644"><div><div><a href="https://github.com/scalanlp/breeze">scalanlp / breeze</a><span></span><span>6 issues</span></div><div>Breeze is/was a nume</div><div><div><span>lang:</span>Scala</div><div><span>stars:</span>3.45K</div><div><span>last activity:</span><span>2 months ago</span></div></div></div></div><div id="repo-2340549"><div><div><a href="https://github.com/playframework/playframework">playframework / play</a><span></span><span>10 issues</span></div><div>The Community Mainta</div><div><div><span>lang:</span>Scala</div><div><span>stars:</span>12.55K</div><div><span>last activity:</span><span>6 days ago</span></div></div></div></div><div id="repo-134079884"><div><div><a href="https://github.com/zio/zio">zio / zio</a><span></span><span>10 issues</span></div><div>ZIO — A type-safe, c</div><div><div><span>lang:</span>Scala</div><div><span>stars:</span>4.08K</div><div><span>last activity:</span><span>2 days ago</span></div></div></div></div></div></section></main></div></div></body>'

data = []
projects = html_data.split('<div id="repo-')
for project in projects[1:]:
    name = project.split('<a href="')[1].split('">')[1].split('</a>')[0]
    issues = project.split('<span>')[2].split(' issues')[0]
    stars = project.split('<span>')[4].split('</span>')[0]
    last_activity = project.split('<span>last activity:</span><span>')[1].split('</span>')[0]
    data.append({'name': name, 'issues': issues, 'stars': stars, 'last_activity': last_activity})

print(json.dumps(data, indent=2))
'''
"""
first_line = parser_logic.split('\n')[1]
last_line = parser_logic.split('\n')[-2]
print('first_line: ', first_line, 'last_line: ', last_line)
new_str =""
if first_line == "'''" and last_line == "'''":
    print("inside")
    #Split the string into lines and copy everything from the second line onward
    lines = parser_logic.splitlines()

    # Join lines starting from the second line (index 2)
    new_str = "\n".join(lines[2:])

    lines = new_str.splitlines()

    new_str = "\n".join(lines[:-2])
    
    #print(new_str)
# execute the code inside new_str
exec(new_str)
