#!/usr/bin/env python3
"""
Harness Integration Test - Validate Agent Coordination System
"""

import os
import json
import asyncio
import websockets
from pathlib import Path
from datetime import datetime

class HarnessIntegrationTest:
    def __init__(self):
        self.test_results = {}
        self.start_time = datetime.now()
        
    def test_documentation_structure(self):
        """Test that all harness documentation exists"""
        print("=== Testing Documentation Structure ===")
        
        required_files = [
            'AGENTS.md',
            'docs/09-PLANNING/Hermes-ACP-Feature-SSoT.md',
            'docs/05-TEST-QA/Regression-SSoT.md',
            'docs/05-TEST-QA/Cadence-Ledger.md',
            'docs/11-REFERENCE/testing-standard.md',
            'docs/11-REFERENCE/execution-workflow-standard.md',
            'docs/11-REFERENCE/docs-library-standard.md',
            'docs/11-REFERENCE/engineering-standard.md',
            'docs/11-REFERENCE/walkthrough-standard.md',
            'docs/11-REFERENCE/worktree-standard.md',
            'docs/11-REFERENCE/regression-ssot-governance.md',
            'docs/09-PLANNING/README.md',
            'docs/10-WALKTHROUGH/README.md',
            'docs/10-WALKTHROUGH/_walkthrough-template.md',
            'docs/09-PLANNING/worktree-tracker.md'
        ]
        
        missing_files = []
        existing_files = []
        
        for file_path in required_files:
            if os.path.exists(file_path):
                existing_files.append(file_path)
            else:
                missing_files.append(file_path)
        
        self.test_results['documentation_structure'] = {
            'status': 'PASS' if not missing_files else 'FAIL',
            'existing_files': len(existing_files),
            'missing_files': missing_files,
            'total_required': len(required_files)
        }
        
        print(f"Required files: {len(required_files)}")
        print(f"Existing files: {len(existing_files)}")
        print(f"Missing files: {len(missing_files)}")
        
        return len(missing_files) == 0
    
    def test_configuration_files(self):
        """Test that configuration files exist and are valid"""
        print("\n=== Testing Configuration Files ===")
        
        config_files = [
            'hermes_acp_config.json',
            'acp_agents_config.json'
        ]
        
        config_results = {}
        
        for config_file in config_files:
            if os.path.exists(config_file):
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config_data = json.load(f)
                    config_results[config_file] = {
                        'status': 'PASS',
                        'valid_json': True,
                        'keys': list(config_data.keys()) if isinstance(config_data, dict) else 'non_dict'
                    }
                    print(f"  {config_file}: VALID")
                except json.JSONDecodeError as e:
                    config_results[config_file] = {
                        'status': 'FAIL',
                        'valid_json': False,
                        'error': str(e)
                    }
                    print(f"  {config_file}: INVALID JSON - {e}")
            else:
                config_results[config_file] = {
                    'status': 'FAIL',
                    'exists': False
                }
                print(f"  {config_file}: MISSING")
        
        self.test_results['configuration_files'] = config_results
        return all(result['status'] == 'PASS' for result in config_results.values())
    
    def test_agent_configuration(self):
        """Test agent configuration in hermes_acp_config.json"""
        print("\n=== Testing Agent Configuration ===")
        
        if not os.path.exists('hermes_acp_config.json'):
            print("  hermes_acp_config.json: MISSING")
            return False
        
        try:
            with open('hermes_acp_config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            required_agents = ['Gemini CLI', 'Windsurf', 'Claude Code', 'Antigravity', 'Hermes']
            agent_servers = config.get('agent_servers', {})
            
            missing_agents = []
            for agent in required_agents:
                if agent not in agent_servers:
                    missing_agents.append(agent)
                else:
                    print(f"  {agent}: CONFIGURED")
            
            if missing_agents:
                print(f"  Missing agents: {missing_agents}")
            
            self.test_results['agent_configuration'] = {
                'status': 'PASS' if not missing_agents else 'FAIL',
                'configured_agents': list(agent_servers.keys()),
                'missing_agents': missing_agents
            }
            
            return len(missing_agents) == 0
            
        except Exception as e:
            print(f"  Error reading config: {e}")
            self.test_results['agent_configuration'] = {
                'status': 'FAIL',
                'error': str(e)
            }
            return False
    
    async def test_port_availability(self):
        """Test that required ports are available or in use"""
        print("\n=== Testing Port Availability ===")
        
        expected_ports = {
            33333: 'Hermes ACP Server',
            3000: 'Windsurf ACP',
            3001: 'Claude Code ACP',
            3002: 'Antigravity ACP',
            33334: 'Gemini Hooks Monitor'
        }
        
        port_results = {}
        
        for port, service in expected_ports.items():
            try:
                # Try to connect to check if port is in use
                reader, writer = await asyncio.open_connection('localhost', port)
                writer.close()
                await writer.wait_closed()
                port_results[port] = {
                    'status': 'IN_USE',
                    'service': service
                }
                print(f"  Port {port} ({service}): IN USE")
            except (ConnectionRefusedError, OSError):
                # Port is available
                port_results[port] = {
                    'status': 'AVAILABLE',
                    'service': service
                }
                print(f"  Port {port} ({service}): AVAILABLE")
            except Exception as e:
                port_results[port] = {
                    'status': 'ERROR',
                    'service': service,
                    'error': str(e)
                }
                print(f"  Port {port} ({service}): ERROR - {e}")
        
        self.test_results['port_availability'] = port_results
        return True  # Port availability test always passes
    
    def test_walkthrough_structure(self):
        """Test walkthrough directory structure"""
        print("\n=== Testing Walkthrough Structure ===")
        
        walkthrough_dir = Path('docs/10-WALKTHROUGH')
        
        if not walkthrough_dir.exists():
            print("  Walkthrough directory: MISSING")
            return False
        
        required_items = [
            'README.md',
            '_walkthrough-template.md'
        ]
        
        missing_items = []
        existing_items = []
        
        for item in required_items:
            item_path = walkthrough_dir / item
            if item_path.exists():
                existing_items.append(item)
                print(f"  {item}: EXISTS")
            else:
                missing_items.append(item)
                print(f"  {item}: MISSING")
        
        # Check for actual walkthrough files
        walkthrough_files = list(walkthrough_dir.glob('*.md'))
        walkthrough_files = [f.name for f in walkthrough_files if not f.name.startswith('_') and f.name != 'README.md']
        
        print(f"  Actual walkthroughs: {len(walkthrough_files)} files")
        for wf in walkthrough_files:
            print(f"    - {wf}")
        
        self.test_results['walkthrough_structure'] = {
            'status': 'PASS' if not missing_items else 'FAIL',
            'existing_items': existing_items,
            'missing_items': missing_items,
            'walkthrough_files': walkthrough_files
        }
        
        return len(missing_items) == 0
    
    def test_planning_structure(self):
        """Test planning directory structure"""
        print("\n=== Testing Planning Structure ===")
        
        planning_dir = Path('docs/09-PLANNING')
        
        if not planning_dir.exists():
            print("  Planning directory: MISSING")
            return False
        
        required_items = [
            'README.md',
            'Hermes-ACP-Feature-SSoT.md',
            'worktree-tracker.md',
            'TASKS/_task-template/task_plan.md',
            'TASKS/_task-template/findings.md',
            'TASKS/_task-template/progress.md'
        ]
        
        missing_items = []
        existing_items = []
        
        for item in required_items:
            item_path = planning_dir / item
            if item_path.exists():
                existing_items.append(item)
                print(f"  {item}: EXISTS")
            else:
                missing_items.append(item)
                print(f"  {item}: MISSING")
        
        self.test_results['planning_structure'] = {
            'status': 'PASS' if not missing_items else 'FAIL',
            'existing_items': existing_items,
            'missing_items': missing_items
        }
        
        return len(missing_items) == 0
    
    async def run_all_tests(self):
        """Run all integration tests"""
        print("=== Hermes ACP Harness Integration Test ===")
        print(f"Started at: {self.start_time}")
        print(f"Working directory: {os.getcwd()}")
        
        tests = [
            ('Documentation Structure', self.test_documentation_structure),
            ('Configuration Files', self.test_configuration_files),
            ('Agent Configuration', self.test_agent_configuration),
            ('Port Availability', self.test_port_availability),
            ('Walkthrough Structure', self.test_walkthrough_structure),
            ('Planning Structure', self.test_planning_structure)
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            try:
                if asyncio.iscoroutinefunction(test_func):
                    result = await test_func()
                else:
                    result = test_func()
                results[test_name] = 'PASS' if result else 'FAIL'
            except Exception as e:
                results[test_name] = 'ERROR'
                print(f"  {test_name}: ERROR - {e}")
        
        # Generate summary
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        print("\n" + "="*50)
        print("=== TEST SUMMARY ===")
        print(f"Duration: {duration}")
        print(f"Tests run: {len(tests)}")
        
        passed = sum(1 for r in results.values() if r == 'PASS')
        failed = sum(1 for r in results.values() if r == 'FAIL')
        errors = sum(1 for r in results.values() if r == 'ERROR')
        
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Errors: {errors}")
        
        print("\nDetailed Results:")
        for test_name, result in results.items():
            status_symbol = {
                'PASS': '  ',
                'FAIL': '  ',
                'ERROR': '  '
            }
            print(f"{status_symbol.get(result, '?')} {test_name}: {result}")
        
        # Save results
        self.test_results['summary'] = {
            'start_time': self.start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'duration': str(duration),
            'total_tests': len(tests),
            'passed': passed,
            'failed': failed,
            'errors': errors,
            'individual_results': results
        }
        
        # Save to file
        results_file = 'harness_integration_test_results.json'
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, default=str)
        
        print(f"\nDetailed results saved to: {results_file}")
        
        return passed == len(tests)  # Return True if all tests passed

async def main():
    tester = HarnessIntegrationTest()
    success = await tester.run_all_tests()
    
    if success:
        print("\n  All tests PASSED! Harness integration is ready.")
        return 0
    else:
        print("\n  Some tests FAILED. Check results for details.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
