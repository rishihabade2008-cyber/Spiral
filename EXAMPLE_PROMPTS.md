# 🎯 Jarvis - Example Prompts to Test

Use these prompts to test different aspects of the Jarvis agent. Copy and paste into the chat.

---

## 🚀 Quick Start (Test These First)

### Basic Commands
```
"Create a Python hello world script"
```
**What it does**: Tests basic file creation and Python execution
**Expected**: Creates project/ folder with hello.py

```
"Create a simple Python calculator"
```
**What it does**: Tests multi-step planning and code generation
**Expected**: Generates calculator.py with basic operations

```
"List files in the project"
```
**What it does**: Tests file reading and memory
**Expected**: Shows all created files

---

## 📚 Learning & Memory Testing

### Test Memory Saving
```
"I prefer Python over other languages for projects"
```
**What it does**: Stores preference in Mem0
**Expected**: Remembers this for future tasks

### Test Memory Retrieval
```
"Build a web scraper for me"
```
**What it does**: Retrieves stored preference, uses Python
**Expected**: References your Python preference

### Test Project Memory
```
"Create a Python project with proper structure"
```
**What it does**: Creates organized structure, saves pattern
**Expected**: Folder structure with src/, tests/, README

---

## 🔧 Tool Testing

### File Operations
```
"Create a folder called 'data' with three empty files: config.json, users.csv, log.txt"
```
**What it does**: Tests file manager with multiple operations
**Expected**: Creates folder and three files

### Python Execution
```
"Write a Python script that prints the first 10 Fibonacci numbers"
```
**What it does**: Tests Python code execution
**Expected**: Generates and runs script

### Code with Dependencies
```
"Create a Python script that generates 100 random numbers and calculates their average"
```
**What it does**: Tests complex code generation
**Expected**: Script with statistics

---

## 🎓 Advanced Testing

### Multi-Step Task
```
"Create a Python project for a todo app with:
1. A data.json file to store todos
2. A main.py script to manage todos
3. A README with instructions"
```
**What it does**: Multi-step planning and execution
**Expected**: Full project with 3 components

### Error Recovery
```
"Create a Python script with intentional syntax error"
```
**What it does**: Tests error detection and reflection
**Expected**: Detects error, shows in reflection

### Task Completion
```
"Build a complete Python calculator with:
- Addition, subtraction, multiplication, division
- Input validation
- Error handling
- Comments explaining the code"
```
**What it does**: Complex task with multiple requirements
**Expected**: Full-featured calculator.py

---

## 💾 Memory-Dependent Tasks

### After learning preferences
```
"Build a project the way I like it"
```
**What it does**: Uses learned preferences
**Expected**: Applies your style

### Building on previous work
```
"Extend the calculator with these features: square root, power, percentage"
```
**What it does**: References previous project
**Expected**: Adds new functions

---

## 🔄 Loop Testing

### Simple Request (Test Analyzer)
```
"What should I build?"
```
**Expected**: Analyzer identifies as chat intent

### Research Request (Test Planner)
```
"Plan a Python machine learning project"
```
**Expected**: Creates structured plan

### Execution Heavy (Test Executor)
```
"Generate 5 Python scripts in different styles"
```
**Expected**: Multiple file creations

### Retry Scenario (Test Reflection)
```
"Create a file with very long content"
```
**Expected**: May need retry, shows reflection

---

## 🎯 Domain-Specific

### Web Development
```
"Create a simple Python Flask app structure"
```

### Data Science
```
"Create a Python data analysis template"
```

### API Development
```
"Create a Python API project structure with FastAPI"
```

### Testing
```
"Create a Python project with unit tests"
```

---

## 📊 Observing the Loop

For each prompt, watch the right panel to see:

1. **🔍 Analyzer** - Understanding the request
   - What intent did it detect?
   - What goal did it extract?

2. **💾 Memory Retriever** - Finding context
   - What memories were found?
   - How are they relevant?

3. **📋 Planner** - Creating plan
   - How many steps?
   - What tools will be used?

4. **⚙️ Executor** - Doing work
   - Which tool ran?
   - Did it succeed?

5. **👁️ Observer** - Recording results
   - What was observed?
   - Were there errors?

6. **🧠 Reflection** - Deciding next step
   - Was it successful?
   - Should we retry?

7. **📚 Learning** - Saving knowledge
   - What was learned?
   - Saved to memory?

---

## 🐛 Testing Error Handling

### Trigger Retry Logic
```
"Create a file in a non-existent directory"
```

### Test Error Detection
```
"Run invalid Python code"
```

### Test Recovery
```
"Try this and fix any errors automatically"
```

---

## 🚀 Progressive Testing

### Level 1: Basic (Start here)
1. "Create a Python hello world script"
2. "List files in the project"
3. "Create a simple Python calculator"

### Level 2: Intermediate
1. "Create a Python project structure"
2. "Remember that I prefer clean code with comments"
3. "Build another project using that preference"

### Level 3: Advanced
1. "Create multiple Python scripts"
2. "Generate tests for them"
3. "Create documentation"
4. "Ask it to recall your preferences"

### Level 4: Expert
1. Complex multi-tool tasks
2. Task recovery and retries
3. Memory-driven decisions
4. Customized workflows

---

## 📈 Performance Testing

### Measure Loop Speed
```
"Create a simple Python script"
```
- Time from send to receive: ~10-20 seconds
- Check: How many loop iterations?

### Measure Memory Impact
After 5 tasks:
```
"How many things have I asked you to remember?"
```
- Tests: Memory retrieval and learning accumulation

---

## 🎓 Learning Progression

### Task 1: Establish Preferences
```
"I like Python. I prefer clean folder structures. Add comments to code."
```

### Task 2: Use Preferences
```
"Create a data processing project"
```
Watch it automatically apply your preferences!

### Task 3: Refine Understanding
```
"Actually, use a different structure this time"
```
Tests: Can it handle preferences changing?

### Task 4: Complex Decisions
```
"Build a project combining everything you know about my style"
```

---

## 💡 Pro Tips

1. **Read the logs** - Terminal shows detailed execution
2. **Watch the loop** - Right panel shows each step
3. **Check learnings** - See what it remembered
4. **Test retrieval** - Ask it about past tasks
5. **Incremental requests** - Build on previous work

---

## 🔍 Prompts for Specific Testing

### Test Semantic Search
```
"Build a machine learning project"
```
Then later:
```
"Create an AI project"
```
Does it find similar memories?

### Test Tool Routing
```
"Create a Python file and also list the project contents"
```

### Test Plan Generation
```
"Create a complete Python project with: structure, code, tests, README, config"
```

### Test Error Handling
```
"Create a Python script with a bug and then fix it"
```

---

## 📝 Your Custom Prompts

As you explore, save prompts that work well:

```
Your favorite prompt:
___________________________________

Another one:
___________________________________

Best one:
___________________________________
```

---

## 🎯 What to Observe

For **each prompt**, note:

- ⏱️ **Execution time**: How fast?
- 🧠 **Plan quality**: Did it understand?
- ✅ **Success rate**: Did it work?
- 💾 **Memory usage**: Did it learn?
- 🔄 **Retries**: Any failures?
- 📊 **Loop count**: How many iterations?

---

## 🚀 Next Level

Once you're comfortable:

1. **Modify prompts** - Customize node behavior
2. **Add tools** - Web search, API calls, GitHub
3. **Extend memory** - New memory types
4. **Build UI** - Custom dashboard
5. **Deploy** - Production server

---

**Start with the Quick Start section above, then explore progressive levels.**

Each task teaches the agent something new. Watch it get smarter over time. 🧠

Happy testing! 🚀
